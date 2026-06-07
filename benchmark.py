# benchmark.py
# Performance measurement and complexity verification

import time
import random

class Benchmark:
    def __init__(self, social_network):
        self.sn = social_network
    
    def run_all_benchmarks(self):
        """Run all benchmarks and print results"""
        print("=" * 60)
        print("PERFORMANCE BENCHMARK - SOCIAL NETWORK")
        print("=" * 60)
        
        self.benchmark_hash_map_lookup()
        self.benchmark_graph_operations()
        self.benchmark_bfs_mutual_friends()
        self.benchmark_heap_recommendations()
        self.benchmark_sorting()
        self.benchmark_binary_search()
        
        print("\n" + "=" * 60)
        print("COMPLEXITY SUMMARY")
        print("=" * 60)
        self.print_complexity_summary()
    
    def benchmark_hash_map_lookup(self):
        """Test O(1) hash map performance"""
        print("\n[HASH MAP LOOKUP - O(1)]")
        
        user_ids = list(self.sn.user_manager.users.keys())
        if len(user_ids) < 100:
            # Add test users
            for i in range(1000):
                self.sn.user_manager.add_user(f"BenchUser_{i}")
            user_ids = list(self.sn.user_manager.users.keys())
        
        start = time.time()
        iterations = 10000
        for _ in range(iterations):
            uid = random.choice(user_ids)
            self.sn.user_manager.get_user(uid)
        elapsed = time.time() - start
        
        print(f"  {iterations} lookups: {elapsed:.4f} seconds")
        print(f"  Average: {elapsed/iterations:.7f} sec per lookup")
        print(f"  Theoretical: O(1) - constant time regardless of data size")
    
    def benchmark_graph_operations(self):
        """Test graph operations"""
        print("\n[GRAPH OPERATIONS - O(1) for add/check]")
        
        users = list(self.sn.user_manager.users.keys())
        if len(users) < 2:
            print("  Not enough users")
            return
        
        start = time.time()
        iterations = 5000
        for _ in range(iterations):
            u1 = random.choice(users)
            u2 = random.choice(users)
            self.sn.friend_graph.are_friends(u1, u2)
        elapsed = time.time() - start
        
        print(f"  {iterations} friendship checks: {elapsed:.4f} seconds")
        print(f"  Theoretical: O(1) per check (hash set lookup)")
    
    def benchmark_bfs_mutual_friends(self):
        """Test BFS + queue performance - O(V+E)"""
        print("\n[BFS MUTUAL FRIENDS - O(V+E)]")
        
        users = list(self.sn.user_manager.users.keys())
        if len(users) < 10:
            print("  Need more users for BFS benchmark")
            return
        
        start = time.time()
        iterations = 50
        for _ in range(iterations):
            u1 = random.choice(users)
            u2 = random.choice(users)
            self.sn.bfs_finder.find_mutual_friends(u1, u2)
        elapsed = time.time() - start
        
        print(f"  {iterations} mutual friend queries: {elapsed:.4f} seconds")
        print(f"  Average: {elapsed/iterations:.4f} sec per query")
        print(f"  Theoretical: O(V+E) where V=users, E=friendships")
    
    def benchmark_heap_recommendations(self):
        """Test heap-based top-K recommendations - O(n log k)"""
        print("\n[HEAP RECOMMENDATIONS - O(n log k)]")
        
        users = list(self.sn.user_manager.users.keys())
        if not users:
            print("  No users for heap benchmark")
            return
        
        start = time.time()
        iterations = 100
        for _ in range(iterations):
            user = random.choice(users)
            self.sn.recommendation_engine.recommend_friends(user, top_k=5)
        elapsed = time.time() - start
        
        print(f"  {iterations} recommendations: {elapsed:.4f} seconds")
        print(f"  Average: {elapsed/iterations:.4f} sec per recommendation")
        print(f"  Theoretical: O(n log k) where n=candidates, k=top_k")
    
    def benchmark_sorting(self):
        """Test O(n log n) sorting"""
        print("\n[SORTING - O(n log n)]")
        
        users = list(self.sn.user_manager.users.keys())
        if not users:
            print("  No users for sorting benchmark")
            return
        
        # Find a user with friends
        for uid in users:
            friends = self.sn.friend_graph.get_friends(uid)
            if len(friends) > 5:
                start = time.time()
                for _ in range(1000):
                    self.sn.sorting_utils.get_sorted_friends(uid)
                elapsed = time.time() - start
                
                print(f"  1,000 sorts of {len(friends)} friends: {elapsed:.4f} seconds")
                print(f"  Theoretical: O(n log n) with n={len(friends)}")
                return
        
        print("  No user with enough friends for sorting benchmark")
    
    def benchmark_binary_search(self):
        """Test O(log n) binary search"""
        print("\n[BINARY SEARCH - O(log n)]")
        
        users = list(self.sn.user_manager.users.keys())
        if not users:
            print("  No users for binary search benchmark")
            return
        
        for uid in users:
            friends = self.sn.friend_graph.get_friends(uid)
            if friends:
                start = time.time()
                for _ in range(5000):
                    self.sn.sorting_utils.binary_search_friend(uid, "ZZZ_NotExist")
                elapsed = time.time() - start
                
                print(f"  5,000 binary searches: {elapsed:.5f} seconds")
                print(f"  Average: {elapsed/5000:.7f} sec per search")
                print(f"  Theoretical: O(log n) where n={len(friends)}")
                break
    
    def print_complexity_summary(self):
        """Print Big-O summary table"""
        print("""
+--------------------------+-------------------+-----------------+------------------+
| Operation                | Data Structure    | Time Complexity | Space Complexity |
+--------------------------+-------------------+-----------------+------------------+
| User lookup by ID        | Hash Map          | O(1)            | O(n)             |
| Add/remove friend        | Graph (adj list)  | O(1)            | O(V+E)           |
| Undo last action         | Stack             | O(1)            | O(h)             |
| Mutual friends (BFS)     | Queue + Hash Map  | O(V+E)          | O(V)             |
| Top-K recommendations    | Min-Heap          | O(n log k)      | O(k)             |
| Sort friends list        | Timsort           | O(n log n)      | O(n)             |
| Find friend by name      | Binary Search     | O(log n)        | O(1)             |
| Get user by name (linear)| Array scan        | O(n)            | O(1)             |
+--------------------------+-------------------+-----------------+------------------+
""")
