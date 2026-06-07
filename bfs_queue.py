# bfs_queue.py
# BFS using Queue for mutual friend discovery and shortest path
# Data structure: Queue (deque) for BFS traversal

from collections import deque

class BFSFriendFinder:
    def __init__(self, friend_graph):
        self.friend_graph = friend_graph
    
    def find_mutual_friends(self, user1_id, user2_id):
        """
        Find mutual friends using hash map counting.
        Returns list of user IDs that are friends with both users.
        """
        friends1 = self.friend_graph.get_friends(user1_id)
        friends2 = self.friend_graph.get_friends(user2_id)
        
        # Use hash map for O(1) counting
        count_map = {}
        for friend in friends1:
            count_map[friend] = count_map.get(friend, 0) + 1
        for friend in friends2:
            count_map[friend] = count_map.get(friend, 0) + 1
        
        # Friends that appear in both (count == 2)
        mutual = [f for f, count in count_map.items() if count == 2]
        return mutual
    
    def bfs_shortest_path(self, start_id, target_id):
        """
        Find shortest path between two users using BFS with queue.
        Returns list of user IDs on shortest path.
        """
        if start_id == target_id:
            return [start_id]
        
        visited = {start_id}
        # Queue stores (current_node, path_to_node)
        queue = deque([(start_id, [start_id])])
        
        while queue:
            current, path = queue.popleft()  # Queue operation: O(1)
            
            for neighbor in self.friend_graph.get_friends(current):
                if neighbor == target_id:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None  # No path found
    
    def bfs_level_order(self, start_id, max_depth=2):
        """
        BFS level order traversal up to max_depth.
        Uses queue to process level by level.
        """
        if start_id not in self.friend_graph.adjacency:
            return []
        
        visited = {start_id}
        queue = deque([(start_id, 0)])  # (user_id, depth)
        result = {0: [start_id]}
        
        while queue:
            user_id, depth = queue.popleft()
            
            if depth >= max_depth:
                continue
            
            for neighbor in self.friend_graph.get_friends(user_id):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
                    
                    if depth + 1 not in result:
                        result[depth + 1] = []
                    result[depth + 1].append(neighbor)
        
        return result
    
    def get_friends_at_distance(self, start_id, distance):
        """
        Get all users at exact distance using BFS.
        """
        levels = self.bfs_level_order(start_id, distance + 1)
        return levels.get(distance, [])
    
    def are_connected(self, user1_id, user2_id):
        """Check if two users are connected (has path) using BFS"""
        return self.bfs_shortest_path(user1_id, user2_id) is not None