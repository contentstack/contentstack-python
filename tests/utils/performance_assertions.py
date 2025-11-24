"""
Performance Assertions - Utilities for performance testing
Based on TypeScript SDK patterns (avoiding flaky strict assertions)
"""

import time
import logging
from typing import Callable, Any, Optional, Dict, List
from functools import wraps


class PerformanceAssertion:
    """
    Performance testing utilities
    
    Note: Based on TS SDK learnings - we LOG performance instead of strict assertions
    to avoid flaky tests due to network/cache variations
    
    Usage:
        timer = PerformanceAssertion.start_timer()
        # ... operation ...
        elapsed = PerformanceAssertion.end_timer(timer, "fetch_operation")
        
        # Or use context manager:
        with PerformanceAssertion.Timer("operation_name") as timer:
            # ... operation ...
            pass
        print(f"Elapsed: {timer.elapsed_ms}ms")
    """
    
    # === TIMER CONTEXT MANAGER ===
    
    class Timer:
        """Context manager for timing operations"""
        def __init__(self, name: str):
            self.name = name
            self.start_time = None
            self.end_time = None
            self.elapsed_ms = None
            self._logger = logging.getLogger(__name__)
        
        def __enter__(self):
            self.start_time = time.perf_counter()
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.end_time = time.perf_counter()
            self.elapsed_ms = (self.end_time - self.start_time) * 1000
            self._logger.info(f"⏱️ {self.name}: {self.elapsed_ms:.2f}ms")
            return False  # Don't suppress exceptions
    
    # === TIMING UTILITIES ===
    
    @staticmethod
    def start_timer() -> float:
        """
        Start a performance timer
        
        Returns:
            Start time in seconds
        
        Example:
            timer = PerformanceAssertion.start_timer()
        """
        return time.time()
    
    @staticmethod
    def end_timer(start_time: float, operation_name: str = "operation") -> float:
        """
        End timer and log elapsed time
        
        Args:
            start_time: Start time from start_timer()
            operation_name: Name of operation for logging
        
        Returns:
            Elapsed time in milliseconds
        
        Example:
            elapsed_ms = PerformanceAssertion.end_timer(timer, "fetch_entry")
        """
        end_time = time.time()
        elapsed_ms = (end_time - start_time) * 1000
        
        logging.info(f"⏱️  [{operation_name}] completed in {elapsed_ms:.2f}ms")
        
        return elapsed_ms
    
    @staticmethod
    def measure_operation(func: Callable, operation_name: str = "operation", *args, **kwargs):
        """
        Measure execution time of a function
        
        Args:
            func: Function to measure
            operation_name: Name for logging
            *args, **kwargs: Arguments to pass to function
        
        Returns:
            Tuple of (result, elapsed_time_ms)
        
        Example:
            result, time_ms = PerformanceAssertion.measure_operation(
                entry.fetch, "fetch_complex_entry"
            )
        """
        start = PerformanceAssertion.start_timer()
        result = func(*args, **kwargs)
        elapsed = PerformanceAssertion.end_timer(start, operation_name)
        
        return (result, elapsed)
    
    # === COMPARISON UTILITIES (Informational, not strict) ===
    
    @staticmethod
    def compare_operations(
        name1: str,
        time1_ms: float,
        name2: str,
        time2_ms: float,
        log_ratio: bool = True
    ):
        """
        Compare performance of two operations (informational only)
        
        Based on TS SDK learning: Don't assert strict comparisons (flaky!)
        Instead, log the comparison for information
        
        Args:
            name1: Name of first operation
            time1_ms: Time of first operation (ms)
            name2: Name of second operation  
            time2_ms: Time of second operation (ms)
            log_ratio: Whether to log the ratio
        
        Example:
            PerformanceAssertion.compare_operations(
                "first_query", first_time,
                "cached_query", cached_time
            )
        """
        logging.info(f"📊 Performance Comparison:")
        logging.info(f"   {name1}: {time1_ms:.2f}ms")
        logging.info(f"   {name2}: {time2_ms:.2f}ms")
        
        if log_ratio and time1_ms > 0:
            ratio = time2_ms / time1_ms
            logging.info(f"   Ratio: {ratio:.2f}x")
            
            if ratio < 1.0:
                logging.info(f"   ✅ {name2} is {(1/ratio):.2f}x faster")
            elif ratio > 1.0:
                logging.info(f"   ⚠️  {name2} is {ratio:.2f}x slower")
            else:
                logging.info(f"   ℹ️  Times are equivalent")
    
    @staticmethod
    def log_operation_times(operations: Dict[str, float]):
        """
        Log multiple operation times
        
        Args:
            operations: Dictionary of {operation_name: time_ms}
        
        Example:
            PerformanceAssertion.log_operation_times({
                "simple_query": 45.2,
                "medium_query": 89.5,
                "complex_query": 234.7
            })
        """
        logging.info("📊 Operation Times:")
        for name, time_ms in sorted(operations.items(), key=lambda x: x[1]):
            logging.info(f"   {name}: {time_ms:.2f}ms")
    
    # === SOFT ASSERTIONS (Log warnings instead of failing) ===
    
    @staticmethod
    def assert_reasonable_time(
        operation_name: str,
        elapsed_ms: float,
        expected_max_ms: float,
        fail_on_slow: bool = False
    ) -> bool:
        """
        Assert operation completed in reasonable time
        
        Args:
            operation_name: Name of operation
            elapsed_ms: Actual elapsed time
            expected_max_ms: Expected maximum time
            fail_on_slow: If True, raise assertion; if False, log warning
        
        Returns:
            True if within expected time
        
        Example:
            # Just log if slow (recommended)
            PerformanceAssertion.assert_reasonable_time(
                "fetch_entry", elapsed, 1000, fail_on_slow=False
            )
        """
        is_reasonable = elapsed_ms <= expected_max_ms
        
        if not is_reasonable:
            message = f"⚠️  {operation_name} took {elapsed_ms:.2f}ms (expected <{expected_max_ms}ms)"
            
            if fail_on_slow:
                raise AssertionError(message)
            else:
                logging.warning(message)
        
        return is_reasonable
    
    @staticmethod
    def assert_faster_than(
        operation_name: str,
        elapsed_ms: float,
        baseline_ms: float,
        tolerance_pct: float = 10.0,
        fail_on_slow: bool = False
    ) -> bool:
        """
        Assert operation is faster than baseline (with tolerance)
        
        Args:
            operation_name: Name of operation
            elapsed_ms: Actual elapsed time
            baseline_ms: Baseline time to compare against
            tolerance_pct: Tolerance percentage (default 10%)
            fail_on_slow: If True, raise assertion; if False, log warning
        
        Returns:
            True if faster (within tolerance)
        
        Example:
            # Allow 10% slower, just log if worse
            PerformanceAssertion.assert_faster_than(
                "cached_query", cached_time, first_time,
                tolerance_pct=10.0, fail_on_slow=False
            )
        """
        max_allowed = baseline_ms * (1 + tolerance_pct / 100)
        is_faster = elapsed_ms <= max_allowed
        
        if not is_faster:
            ratio = elapsed_ms / baseline_ms
            message = (
                f"⚠️  {operation_name} ({elapsed_ms:.2f}ms) is slower than baseline "
                f"({baseline_ms:.2f}ms) by {ratio:.2f}x (tolerance: {tolerance_pct}%)"
            )
            
            if fail_on_slow:
                raise AssertionError(message)
            else:
                logging.warning(message)
        
        return is_faster
    
    # === DECORATORS ===
    
    @staticmethod
    def time_it(operation_name: Optional[str] = None):
        """
        Decorator to measure function execution time
        
        Args:
            operation_name: Optional name (defaults to function name)
        
        Example:
            @PerformanceAssertion.time_it("fetch_complex_entry")
            def fetch_entry(self):
                return self.stack.content_type('ct').entry('uid').fetch()
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                name = operation_name or func.__name__
                start = PerformanceAssertion.start_timer()
                result = func(*args, **kwargs)
                PerformanceAssertion.end_timer(start, name)
                return result
            return wrapper
        return decorator
    
    # === BATCH OPERATIONS ===
    
    @staticmethod
    def measure_batch_operations(
        operations: Dict[str, Callable],
        *args,
        **kwargs
    ):
        """
        Measure multiple operations and return results with timings
        
        Args:
            operations: Dictionary of {name: function}
            *args, **kwargs: Arguments to pass to all functions
        
        Returns:
            Dictionary of {name: (result, time_ms)}
        
        Example:
            results = PerformanceAssertion.measure_batch_operations({
                "simple": lambda: simple_query.find(),
                "complex": lambda: complex_query.find()
            })
        """
        results = {}
        
        for name, func in operations.items():
            result, time_ms = PerformanceAssertion.measure_operation(func, name, *args, **kwargs)
            results[name] = (result, time_ms)
        
        # Log summary
        times = {name: time_ms for name, (_, time_ms) in results.items()}
        PerformanceAssertion.log_operation_times(times)
        
        return results
    
    # === MEMORY TRACKING (Basic) ===
    
    @staticmethod
    def log_memory_usage():
        """
        Log current memory usage (if psutil available)
        
        Example:
            PerformanceAssertion.log_memory_usage()
        """
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            logging.info(f"💾 Memory usage: {memory_mb:.2f} MB")
            
        except ImportError:
            logging.debug("psutil not available - skipping memory logging")
    
    # === STATISTICAL HELPERS ===
    
    @staticmethod
    def calculate_stats(times: List[float]) -> Dict[str, float]:
        """
        Calculate statistics for a list of times
        
        Args:
            times: List of time measurements (ms)
        
        Returns:
            Dictionary with min, max, avg, median
        
        Example:
            stats = PerformanceAssertion.calculate_stats(all_times)
            logging.info(f"Average: {stats['avg']:.2f}ms")
        """
        if not times:
            return {}
        
        sorted_times = sorted(times)
        n = len(sorted_times)
        
        return {
            'min': sorted_times[0],
            'max': sorted_times[-1],
            'avg': sum(times) / n,
            'median': sorted_times[n // 2] if n % 2 == 1 else (sorted_times[n//2-1] + sorted_times[n//2]) / 2
        }
    
    @staticmethod
    def log_stats(operation_name: str, times: List[float]):
        """
        Log statistics for multiple runs
        
        Args:
            operation_name: Name of operation
            times: List of time measurements (ms)
        
        Example:
            times = [45.2, 48.1, 43.9, 47.3, 46.8]
            PerformanceAssertion.log_stats("query_operation", times)
        """
        stats = PerformanceAssertion.calculate_stats(times)
        
        logging.info(f"📈 Stats for {operation_name} ({len(times)} runs):")
        logging.info(f"   Min: {stats['min']:.2f}ms")
        logging.info(f"   Max: {stats['max']:.2f}ms")
        logging.info(f"   Avg: {stats['avg']:.2f}ms")
        logging.info(f"   Median: {stats['median']:.2f}ms")

