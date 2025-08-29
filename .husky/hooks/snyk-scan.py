#!/usr/bin/env python3
"""
Snyk security scanning hook for Husky-style pre-commit setup.
This hook runs Snyk security scanning on Python dependencies.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def run_snyk_scan():
    """Run Snyk security scan on Python dependencies."""
    
    # Check if Snyk CLI is available
    try:
        subprocess.run(['snyk', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Snyk CLI not found. Please install it first:")
        print("   npm install -g snyk")
        print("   or visit: https://snyk.io/docs/using-snyk/")
        return 1
    
    # Check if SNYK_TOKEN is set
    if not os.getenv('SNYK_TOKEN'):
        print("⚠️  SNYK_TOKEN environment variable not set.")
        print("   Please set it with: export SNYK_TOKEN=your_token")
        print("   You can get a token from: https://app.snyk.io/account")
        return 0  # Don't fail the commit, just warn
    
    # Check for requirements.txt
    requirements_files = ['requirements.txt', 'setup.py']
    found_requirements = False
    
    for req_file in requirements_files:
        if Path(req_file).exists():
            found_requirements = True
            break
    
    if not found_requirements:
        print("⚠️  No requirements.txt or setup.py found. Skipping Snyk scan.")
        return 0
    
    print("🔍 Running Snyk security scan...")
    
    try:
        # Run Snyk test on Python dependencies
        result = subprocess.run([
            'snyk', 'test',
            '--severity-threshold=high',
            '--json'
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("✅ Snyk scan completed - no high severity vulnerabilities found")
            return 0
        else:
            # Parse JSON output to show vulnerabilities
            try:
                vulns = json.loads(result.stdout)
                if 'vulnerabilities' in vulns:
                    print("❌ High severity vulnerabilities found:")
                    for vuln in vulns['vulnerabilities']:
                        if vuln.get('severity') == 'high':
                            print(f"   - {vuln.get('title', 'Unknown')} in {vuln.get('packageName', 'Unknown')}")
                            print(f"     CVSS Score: {vuln.get('cvssScore', 'N/A')}")
                            print(f"     More info: {vuln.get('url', 'N/A')}")
                            print()
                
                print("💡 To fix vulnerabilities, run: snyk wizard")
                return 1
            except json.JSONDecodeError:
                print("❌ Snyk scan failed with errors:")
                print(result.stderr)
                return 1
                
    except Exception as e:
        print(f"❌ Error running Snyk scan: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(run_snyk_scan())
