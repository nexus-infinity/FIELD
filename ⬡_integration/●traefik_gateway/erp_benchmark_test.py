#!/usr/bin/env python3
"""
ERP Benchmark Testing Framework
Performance testing tools to measure the dynamic ERP system against industry standards
"""

import asyncio
import aiohttp
import time
import json
import statistics
from datetime import datetime
from typing import List, Dict, Any
import concurrent.futures
import requests
from dataclasses import dataclass
import threading

@dataclass
class BenchmarkResult:
    test_name: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    p95_response_time: float
    throughput_per_second: float
    error_rate: float
    start_time: datetime
    end_time: datetime
    duration: float

class ERPBenchmarkTester:
    """Comprehensive ERP system performance testing framework"""
    
    def __init__(self, base_url: str = "http://localhost:5006"):
        self.base_url = base_url
        self.results: List[BenchmarkResult] = []
        
    def run_all_benchmarks(self):
        """Execute all benchmark tests"""
        print("🚀 Starting ERP Benchmark Test Suite")
        print("=" * 60)
        
        # Test scenarios
        tests = [
            ("Dashboard Load Test", self.benchmark_dashboard_load),
            ("API Response Time Test", self.benchmark_api_response_time),
            ("Concurrent Users Test", self.benchmark_concurrent_users),
            ("Trade Creation Stress Test", self.benchmark_trade_creation),
            ("Database Query Performance", self.benchmark_database_queries),
            ("Workflow Processing Test", self.benchmark_workflow_processing)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🧪 Running {test_name}...")
            try:
                result = test_func()
                self.results.append(result)
                self._print_result(result)
            except Exception as e:
                print(f"❌ Test failed: {e}")
                
        self._generate_benchmark_report()
        
    def benchmark_dashboard_load(self) -> BenchmarkResult:
        """Test dashboard page load performance"""
        test_name = "Dashboard Load Performance"
        num_requests = 100
        response_times = []
        successful = 0
        failed = 0
        
        start_time = datetime.now()
        
        for i in range(num_requests):
            try:
                start = time.time()
                response = requests.get(f"{self.base_url}/", timeout=10)
                end = time.time()
                
                response_time = end - start
                response_times.append(response_time)
                
                if response.status_code == 200:
                    successful += 1
                else:
                    failed += 1
                    
            except Exception as e:
                failed += 1
                print(f"Request {i+1} failed: {e}")
                
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return BenchmarkResult(
            test_name=test_name,
            total_requests=num_requests,
            successful_requests=successful,
            failed_requests=failed,
            avg_response_time=statistics.mean(response_times) if response_times else 0,
            min_response_time=min(response_times) if response_times else 0,
            max_response_time=max(response_times) if response_times else 0,
            p95_response_time=statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
            throughput_per_second=successful / duration if duration > 0 else 0,
            error_rate=(failed / num_requests) * 100,
            start_time=start_time,
            end_time=end_time,
            duration=duration
        )
        
    def benchmark_api_response_time(self) -> BenchmarkResult:
        """Test API endpoint response times"""
        test_name = "API Response Time"
        endpoints = [
            "/health",
            "/api/metrics", 
            "/api/trades",
            "/api/workflow/trade_001"
        ]
        
        response_times = []
        successful = 0
        failed = 0
        total_requests = 0
        
        start_time = datetime.now()
        
        for endpoint in endpoints:
            for i in range(25):  # 25 requests per endpoint
                try:
                    start = time.time()
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                    end = time.time()
                    
                    response_time = end - start
                    response_times.append(response_time)
                    total_requests += 1
                    
                    if response.status_code == 200:
                        successful += 1
                    else:
                        failed += 1
                        
                except Exception as e:
                    failed += 1
                    total_requests += 1
                    
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return BenchmarkResult(
            test_name=test_name,
            total_requests=total_requests,
            successful_requests=successful,
            failed_requests=failed,
            avg_response_time=statistics.mean(response_times) if response_times else 0,
            min_response_time=min(response_times) if response_times else 0,
            max_response_time=max(response_times) if response_times else 0,
            p95_response_time=statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
            throughput_per_second=successful / duration if duration > 0 else 0,
            error_rate=(failed / total_requests) * 100 if total_requests > 0 else 0,
            start_time=start_time,
            end_time=end_time,
            duration=duration
        )
        
    def benchmark_concurrent_users(self) -> BenchmarkResult:
        """Test system performance under concurrent user load"""
        test_name = "Concurrent Users Load Test"
        num_users = 50
        requests_per_user = 10
        
        response_times = []
        successful = 0
        failed = 0
        
        start_time = datetime.now()
        
        def user_simulation(user_id: int):
            user_response_times = []
            user_successful = 0
            user_failed = 0
            
            for i in range(requests_per_user):
                try:
                    start = time.time()
                    
                    # Simulate realistic user behavior
                    if i % 3 == 0:
                        response = requests.get(f"{self.base_url}/")
                    elif i % 3 == 1:
                        response = requests.get(f"{self.base_url}/api/metrics")
                    else:
                        response = requests.get(f"{self.base_url}/api/trades")
                        
                    end = time.time()
                    response_time = end - start
                    user_response_times.append(response_time)
                    
                    if response.status_code == 200:
                        user_successful += 1
                    else:
                        user_failed += 1
                        
                    # Simulate user think time
                    time.sleep(0.1)
                    
                except Exception as e:
                    user_failed += 1
                    
            return user_response_times, user_successful, user_failed
            
        # Use thread pool for concurrent execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_users) as executor:
            future_to_user = {
                executor.submit(user_simulation, user_id): user_id 
                for user_id in range(num_users)
            }
            
            for future in concurrent.futures.as_completed(future_to_user):
                user_times, user_success, user_fails = future.result()
                response_times.extend(user_times)
                successful += user_success
                failed += user_fails
                
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        total_requests = num_users * requests_per_user
        
        return BenchmarkResult(
            test_name=test_name,
            total_requests=total_requests,
            successful_requests=successful,
            failed_requests=failed,
            avg_response_time=statistics.mean(response_times) if response_times else 0,
            min_response_time=min(response_times) if response_times else 0,
            max_response_time=max(response_times) if response_times else 0,
            p95_response_time=statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
            throughput_per_second=successful / duration if duration > 0 else 0,
            error_rate=(failed / total_requests) * 100 if total_requests > 0 else 0,
            start_time=start_time,
            end_time=end_time,
            duration=duration
        )
        
    def benchmark_trade_creation(self) -> BenchmarkResult:
        """Test trade creation API under load"""
        test_name = "Trade Creation Stress Test"
        num_trades = 20  # Limited by sample data
        
        response_times = []
        successful = 0
        failed = 0
        
        start_time = datetime.now()
        
        # Sample trade data
        trade_data = [
            {"customer_id": "cust_001", "product_id": "prod_001", "quantity": 10.0},
            {"customer_id": "cust_002", "product_id": "prod_002", "quantity": 15.0},
            {"customer_id": "cust_003", "product_id": "prod_003", "quantity": 5.0},
        ]
        
        for i in range(num_trades):
            try:
                trade = trade_data[i % len(trade_data)]
                trade["quantity"] = trade["quantity"] + (i * 0.1)  # Vary quantities
                
                start = time.time()
                response = requests.post(
                    f"{self.base_url}/api/trades",
                    json=trade,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                end = time.time()
                
                response_time = end - start
                response_times.append(response_time)
                
                if response.status_code in [200, 201]:
                    successful += 1
                    print(f"✅ Created trade {i+1}: {response.json().get('trade_id', 'N/A')}")
                else:
                    failed += 1
                    print(f"❌ Failed to create trade {i+1}: {response.text}")
                    
            except Exception as e:
                failed += 1
                print(f"❌ Trade creation {i+1} failed: {e}")
                
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return BenchmarkResult(
            test_name=test_name,
            total_requests=num_trades,
            successful_requests=successful,
            failed_requests=failed,
            avg_response_time=statistics.mean(response_times) if response_times else 0,
            min_response_time=min(response_times) if response_times else 0,
            max_response_time=max(response_times) if response_times else 0,
            p95_response_time=statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
            throughput_per_second=successful / duration if duration > 0 else 0,
            error_rate=(failed / num_trades) * 100,
            start_time=start_time,
            end_time=end_time,
            duration=duration
        )
        
    def benchmark_database_queries(self) -> BenchmarkResult:
        """Test database query performance through APIs"""
        test_name = "Database Query Performance"
        
        queries = [
            "/api/trades",      # Complex join query
            "/api/metrics",     # Aggregation queries
            "/health",          # Simple status query
        ]
        
        response_times = []
        successful = 0
        failed = 0
        total_requests = 0
        
        start_time = datetime.now()
        
        for query in queries:
            for i in range(50):  # 50 requests per query type
                try:
                    start = time.time()
                    response = requests.get(f"{self.base_url}{query}", timeout=10)
                    end = time.time()
                    
                    response_time = end - start
                    response_times.append(response_time)
                    total_requests += 1
                    
                    if response.status_code == 200:
                        successful += 1
                    else:
                        failed += 1
                        
                except Exception as e:
                    failed += 1
                    total_requests += 1
                    
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return BenchmarkResult(
            test_name=test_name,
            total_requests=total_requests,
            successful_requests=successful,
            failed_requests=failed,
            avg_response_time=statistics.mean(response_times) if response_times else 0,
            min_response_time=min(response_times) if response_times else 0,
            max_response_time=max(response_times) if response_times else 0,
            p95_response_time=statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
            throughput_per_second=successful / duration if duration > 0 else 0,
            error_rate=(failed / total_requests) * 100 if total_requests > 0 else 0,
            start_time=start_time,
            end_time=end_time,
            duration=duration
        )
        
    def benchmark_workflow_processing(self) -> BenchmarkResult:
        """Test workflow API performance"""
        test_name = "Workflow Processing Performance"
        
        # Test workflow status queries
        workflow_ids = ["trade_001", "trade_002", "trade_003"]
        num_requests_per_id = 20
        
        response_times = []
        successful = 0
        failed = 0
        total_requests = 0
        
        start_time = datetime.now()
        
        for workflow_id in workflow_ids:
            for i in range(num_requests_per_id):
                try:
                    start = time.time()
                    response = requests.get(f"{self.base_url}/api/workflow/{workflow_id}", timeout=10)
                    end = time.time()
                    
                    response_time = end - start
                    response_times.append(response_time)
                    total_requests += 1
                    
                    if response.status_code == 200:
                        successful += 1
                    else:
                        failed += 1
                        
                except Exception as e:
                    failed += 1
                    total_requests += 1
                    
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return BenchmarkResult(
            test_name=test_name,
            total_requests=total_requests,
            successful_requests=successful,
            failed_requests=failed,
            avg_response_time=statistics.mean(response_times) if response_times else 0,
            min_response_time=min(response_times) if response_times else 0,
            max_response_time=max(response_times) if response_times else 0,
            p95_response_time=statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
            throughput_per_second=successful / duration if duration > 0 else 0,
            error_rate=(failed / total_requests) * 100 if total_requests > 0 else 0,
            start_time=start_time,
            end_time=end_time,
            duration=duration
        )
        
    def _print_result(self, result: BenchmarkResult):
        """Print benchmark result in formatted way"""
        print(f"\n📊 {result.test_name} Results:")
        print(f"   Total Requests: {result.total_requests}")
        print(f"   Successful: {result.successful_requests} ({100-result.error_rate:.1f}%)")
        print(f"   Failed: {result.failed_requests} ({result.error_rate:.1f}%)")
        print(f"   Average Response Time: {result.avg_response_time*1000:.1f}ms")
        print(f"   95th Percentile: {result.p95_response_time*1000:.1f}ms")
        print(f"   Min/Max: {result.min_response_time*1000:.1f}ms / {result.max_response_time*1000:.1f}ms")
        print(f"   Throughput: {result.throughput_per_second:.1f} requests/second")
        print(f"   Duration: {result.duration:.2f} seconds")
        
        # ERP Benchmark Comparison
        self._compare_to_erp_standards(result)
        
    def _compare_to_erp_standards(self, result: BenchmarkResult):
        """Compare results against ERP industry standards"""
        standards = {
            "response_time_ms": 500,      # <500ms target
            "p95_response_time_ms": 2000, # <2s for 95th percentile
            "error_rate_percent": 0.1,    # <0.1% error rate
            "throughput_min": 10          # >10 requests/second minimum
        }
        
        avg_ms = result.avg_response_time * 1000
        p95_ms = result.p95_response_time * 1000
        
        status_indicators = []
        
        if avg_ms <= standards["response_time_ms"]:
            status_indicators.append("✅ Response Time")
        else:
            status_indicators.append("❌ Response Time")
            
        if p95_ms <= standards["p95_response_time_ms"]:
            status_indicators.append("✅ 95th Percentile")
        else:
            status_indicators.append("❌ 95th Percentile")
            
        if result.error_rate <= standards["error_rate_percent"]:
            status_indicators.append("✅ Error Rate")
        else:
            status_indicators.append("❌ Error Rate")
            
        if result.throughput_per_second >= standards["throughput_min"]:
            status_indicators.append("✅ Throughput")
        else:
            status_indicators.append("❌ Throughput")
            
        print(f"   ERP Standards: {' | '.join(status_indicators)}")
        
    def _generate_benchmark_report(self):
        """Generate comprehensive benchmark report"""
        print("\n" + "=" * 80)
        print("📋 COMPREHENSIVE ERP BENCHMARK REPORT")
        print("=" * 80)
        
        print(f"\n🕐 Test Execution Summary:")
        print(f"   Start Time: {self.results[0].start_time}")
        print(f"   End Time: {self.results[-1].end_time}")
        total_duration = (self.results[-1].end_time - self.results[0].start_time).total_seconds()
        print(f"   Total Duration: {total_duration:.2f} seconds")
        
        # Aggregate statistics
        total_requests = sum(r.total_requests for r in self.results)
        total_successful = sum(r.successful_requests for r in self.results)
        total_failed = sum(r.failed_requests for r in self.results)
        avg_response_times = [r.avg_response_time for r in self.results]
        
        print(f"\n📈 Aggregate Performance Metrics:")
        print(f"   Total Requests Processed: {total_requests:,}")
        print(f"   Overall Success Rate: {(total_successful/total_requests)*100:.2f}%")
        print(f"   Overall Error Rate: {(total_failed/total_requests)*100:.2f}%")
        print(f"   Average Response Time: {statistics.mean(avg_response_times)*1000:.1f}ms")
        print(f"   System Throughput: {total_successful/total_duration:.1f} requests/second")
        
        # ERP Comparison Summary
        print(f"\n⚖️  ERP Industry Benchmark Comparison:")
        
        standards_met = 0
        total_standards = 0
        
        for result in self.results:
            avg_ms = result.avg_response_time * 1000
            p95_ms = result.p95_response_time * 1000
            
            # Check standards
            if avg_ms <= 500: standards_met += 1
            if p95_ms <= 2000: standards_met += 1  
            if result.error_rate <= 0.1: standards_met += 1
            if result.throughput_per_second >= 10: standards_met += 1
            total_standards += 4
            
        compliance_rate = (standards_met / total_standards) * 100
        print(f"   Standards Compliance: {compliance_rate:.1f}% ({standards_met}/{total_standards})")
        
        if compliance_rate >= 90:
            print("   🏆 EXCELLENT - Exceeds ERP industry standards")
        elif compliance_rate >= 75:
            print("   ✅ GOOD - Meets most ERP industry standards")
        elif compliance_rate >= 50:
            print("   ⚠️  ACCEPTABLE - Room for performance improvement")
        else:
            print("   ❌ NEEDS IMPROVEMENT - Below ERP industry standards")
            
        # Recommendations
        print(f"\n💡 Performance Recommendations:")
        
        slow_tests = [r for r in self.results if r.avg_response_time > 0.5]
        if slow_tests:
            print("   • Consider optimizing slow endpoints:")
            for test in slow_tests:
                print(f"     - {test.test_name}: {test.avg_response_time*1000:.1f}ms avg")
                
        high_error_tests = [r for r in self.results if r.error_rate > 0.1]
        if high_error_tests:
            print("   • Address error rates in:")
            for test in high_error_tests:
                print(f"     - {test.test_name}: {test.error_rate:.2f}% errors")
                
        low_throughput_tests = [r for r in self.results if r.throughput_per_second < 10]
        if low_throughput_tests:
            print("   • Improve throughput for:")
            for test in low_throughput_tests:
                print(f"     - {test.test_name}: {test.throughput_per_second:.1f} req/sec")
                
        print(f"\n🎯 Next Steps:")
        print("   1. Monitor system performance in production")
        print("   2. Set up automated performance testing")
        print("   3. Implement performance alerts and dashboards")
        print("   4. Consider horizontal scaling for high-load scenarios")
        print("   5. Optimize database queries and indexing")
        
        # Save detailed results to file
        self._save_results_to_file()
        
    def _save_results_to_file(self):
        """Save benchmark results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"erp_benchmark_results_{timestamp}.json"
        
        results_data = []
        for result in self.results:
            results_data.append({
                "test_name": result.test_name,
                "total_requests": result.total_requests,
                "successful_requests": result.successful_requests,
                "failed_requests": result.failed_requests,
                "avg_response_time_ms": result.avg_response_time * 1000,
                "min_response_time_ms": result.min_response_time * 1000,
                "max_response_time_ms": result.max_response_time * 1000,
                "p95_response_time_ms": result.p95_response_time * 1000,
                "throughput_per_second": result.throughput_per_second,
                "error_rate_percent": result.error_rate,
                "duration_seconds": result.duration,
                "start_time": result.start_time.isoformat(),
                "end_time": result.end_time.isoformat()
            })
            
        with open(filename, 'w') as f:
            json.dump({
                "benchmark_summary": {
                    "timestamp": datetime.now().isoformat(),
                    "system_under_test": "Berjak Dynamic ERP",
                    "test_environment": "Local Development"
                },
                "results": results_data
            }, f, indent=2)
            
        print(f"\n💾 Detailed results saved to: {filename}")

def main():
    """Run ERP benchmark tests"""
    print("🏛️ Berjak ERP System Performance Benchmark")
    print("Testing against modern ERP industry standards...")
    print("\nEnsure the ERP system is running on http://localhost:5006")
    
    # Check if system is running
    try:
        response = requests.get("http://localhost:5006/health", timeout=5)
        if response.status_code == 200:
            print("✅ ERP system is running and healthy")
        else:
            print("❌ ERP system not responding correctly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to ERP system: {e}")
        print("Please start the dynamic ERP system first:")
        print("python berjak_erp_dynamic.py")
        return
        
    # Run benchmarks
    tester = ERPBenchmarkTester()
    tester.run_all_benchmarks()

if __name__ == "__main__":
    main()