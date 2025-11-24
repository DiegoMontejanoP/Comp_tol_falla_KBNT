import requests
import time
import random
import threading
import json
from datetime import datetime
import logging

# Configuration
SERVICES = {
    'add': 'http://localhost:5001/calculate',
    'subtract': 'http://localhost:5002/calculate',
    'multiply': 'http://localhost:5003/calculate',
    'divide': 'http://localhost:5004/calculate'
}


class LoadTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.results = []
        self.operation_counts = {'add': 0, 'subtract': 0, 'multiply': 0, 'divide': 0}
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_response_time': 0
        }

    def simulate_user(self, user_id, num_operations=20):
        """Simulate a user performing calculator operations"""
        for i in range(num_operations):
            # Random operation data
            operation = random.choice(['add', 'subtract', 'multiply', 'divide'])
            num1 = random.uniform(-100, 100)

            # Avoid division by zero
            if operation == 'divide':
                num2 = random.uniform(-50, 50)
                if abs(num2) < 0.1:
                    num2 = 1.0
            else:
                num2 = random.uniform(-50, 50)

            # Track operation
            self.operation_counts[operation] += 1

            # Perform calculation
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}/calculate",
                    json={
                        'num1': num1,
                        'num2': num2,
                        'operation': operation
                    },
                    timeout=5
                )

                response_time = time.time() - start_time

                result = {
                    'user_id': user_id,
                    'operation_id': i,
                    'operation': operation,
                    'numbers': (num1, num2),
                    'timestamp': datetime.now().isoformat(),
                    'response_time': response_time,
                    'status': 'success' if response.status_code == 200 else 'error',
                    'status_code': response.status_code,
                    'result': response.json() if response.status_code == 200 else None
                }

                # Update stats
                self.stats['total_requests'] += 1
                if response.status_code == 200:
                    self.stats['successful_requests'] += 1
                else:
                    self.stats['failed_requests'] += 1
                self.stats['total_response_time'] += response_time

            except Exception as e:
                result = {
                    'user_id': user_id,
                    'operation_id': i,
                    'operation': operation,
                    'numbers': (num1, num2),
                    'timestamp': datetime.now().isoformat(),
                    'response_time': 0,
                    'status': 'error',
                    'status_code': 0,
                    'error': str(e)
                }
                self.stats['failed_requests'] += 1
                self.stats['total_requests'] += 1

            self.results.append(result)

            # Random delay between operations
            time.sleep(random.uniform(0.1, 1.0))

    def run_simulation(self, num_users=5, operations_per_user=20):
        """Run simulation with multiple concurrent users"""
        print(f"Starting simulation with {num_users} users...")
        threads = []

        for user_id in range(num_users):
            thread = threading.Thread(
                target=self.simulate_user,
                args=(user_id, operations_per_user)
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        self.print_stats()
        self.save_results()
        return self.operation_counts

    def print_stats(self):
        """Print simulation statistics"""
        print("\n=== Simulation Statistics ===")
        print(f"Total Requests: {self.stats['total_requests']}")
        print(f"Successful: {self.stats['successful_requests']}")
        print(f"Failed: {self.stats['failed_requests']}")

        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful_requests'] / self.stats['total_requests']) * 100
            avg_response_time = self.stats['total_response_time'] / self.stats['total_requests']
            print(f"Success Rate: {success_rate:.2f}%")
            print(f"Average Response Time: {avg_response_time:.3f}s")

        print("\nOperation Distribution:")
        for op, count in self.operation_counts.items():
            percentage = (count / self.stats['total_requests']) * 100
            print(f"  {op}: {count} ({percentage:.1f}%)")

    def save_results(self):
        """Save results to JSON file for analysis"""
        with open('simulation_results.json', 'w') as f:
            json.dump({
                'stats': self.stats,
                'operation_counts': self.operation_counts,
                'results': self.results,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        print("\nResults saved to simulation_results.json")


if __name__ == '__main__':
    tester = LoadTester()

    # Run different simulation scenarios
    print("1. Light Load (2 users)")
    op_counts_light = tester.run_simulation(num_users=2, operations_per_user=10)

    print("\n2. Medium Load (5 users)")
    op_counts_medium = tester.run_simulation(num_users=5, operations_per_user=15)

    print("\n3. Heavy Load (10 users)")
    op_counts_heavy = tester.run_simulation(num_users=10, operations_per_user=20)

    # Save combined operation counts for visualization
    combined_counts = {
        'light': op_counts_light,
        'medium': op_counts_medium,
        'heavy': op_counts_heavy
    }
    with open('operation_counts.json', 'w') as f:
        json.dump(combined_counts, f, indent=2)