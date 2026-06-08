# recommendation_heap.py
# Top-K friend recommendations using Min-Heap
# Data structure: Heap (priority queue) for top-K selection

import heapq

class RecommendationEngine:
    def __init__(self, friend_graph):
        self.friend_graph = friend_graph
    
    def recommend_friends(self, user_id, top_k=5):
        """
        Recommend friends based on mutual friend count.
        Uses min-heap to keep top K recommendations efficiently.
        Time complexity: O(n log k) where n = number of candidates
        """
        if user_id not in self.friend_graph.adjacency:
            return []
        
        current_friends = self.friend_graph.get_friends(user_id)
        score_map = {}  # Hash map: candidate -> mutual friend count
        
        # Count mutual friends for each candidate
        for friend in current_friends:
            for friend_of_friend in self.friend_graph.get_friends(friend):
                # Don't recommend self or existing friends
                if (friend_of_friend != user_id and 
                    friend_of_friend not in current_friends):
                    score_map[friend_of_friend] = score_map.get(friend_of_friend, 0) + 1
        
        # Min-heap to keep only top K (O(n log k) instead of O(n log n))
        heap = []
        for candidate, score in score_map.items():
            heapq.heappush(heap, (score, candidate))
            if len(heap) > top_k:
                heapq.heappop(heap)  # Remove smallest score
        
        # Extract results in descending order (highest score first)
        result = sorted(heap, reverse=True)
        return [(candidate, score) for score, candidate in result]
    
    def get_top_k_friends(self, user_id, top_k=10):
        """
        Get top K friends based on their friend count (popularity).
        Uses heap to find most connected friends.
        """
        friends = self.friend_graph.get_friends(user_id)
        if not friends:
            return []
        
        # Build heap of (friend_count, friend_id)
        heap = []
        for friend_id in friends:
            count = self.friend_graph.get_friend_count(friend_id)
            heapq.heappush(heap, (count, friend_id))
            if len(heap) > top_k:
                heapq.heappop(heap)
        
        result = sorted(heap, reverse=True)
        return [(friend_id, count) for count, friend_id in result]
    
    def recommend_by_degrees(self, user_id, top_k=5):
        """
        Alternative recommendation: prioritize users with many mutual connections.
        Uses heap for ranking.
        """
        from collections import deque
        
        visited = {user_id}
        queue = deque([(user_id, 0)])
        candidate_scores = {}
        
        while queue:
            current, depth = queue.popleft()
            
            if depth >= 2:
                continue
            
            for neighbor in self.friend_graph.get_friends(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
                    
                    if depth == 1 and neighbor != user_id:
                        # Depth 2 nodes are candidates
                        if neighbor not in self.friend_graph.get_friends(user_id):
                            candidate_scores[neighbor] = candidate_scores.get(neighbor, 0) + 1
        
        # Use heap for top K
        heap = [(score, cand) for cand, score in candidate_scores.items()]
        heapq.heapify(heap)
        
        # Extract largest K
        result = []
        while heap and len(result) < top_k:
            score, cand = heapq.heappop(heap)
            result.append((cand, score))
        
        return sorted(result, reverse=True)
