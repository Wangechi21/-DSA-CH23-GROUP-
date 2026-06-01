# friend_graph.py
# Graph implementation for friend connections (adjacency list)
# Data structure: Graph with adjacency list representation

class FriendGraph:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        # Graph as adjacency list: user_id -> set of friend_ids
        self.adjacency = {}
    
    def add_friend(self, user1_id, user2_id):
        """Add bidirectional friendship edge"""
        if user1_id not in self.adjacency:
            self.adjacency[user1_id] = set()
        if user2_id not in self.adjacency:
            self.adjacency[user2_id] = set()
        
        self.adjacency[user1_id].add(user2_id)
        self.adjacency[user2_id].add(user1_id)
        return True
    
    def remove_friend(self, user1_id, user2_id):
        """Remove friendship edge"""
        if user1_id in self.adjacency:
            self.adjacency[user1_id].discard(user2_id)
        if user2_id in self.adjacency:
            self.adjacency[user2_id].discard(user1_id)
        return True
    
    def get_friends(self, user_id):
        """Return set of friends for a user"""
        return self.adjacency.get(user_id, set()).copy()
    
    def are_friends(self, user1_id, user2_id):
        """Check if two users are friends"""
        return (user2_id in self.adjacency.get(user1_id, set()))
    
    def get_friend_count(self, user_id):
        """Return number of friends (degree in graph)"""
        return len(self.adjacency.get(user_id, set()))
    
    def get_all_friendships(self):
        """Return all friendships as list of tuples"""
        friendships = []
        seen = set()
        for u1, friends in self.adjacency.items():
            for u2 in friends:
                if (u2, u1) not in seen:
                    friendships.append((u1, u2))
                    seen.add((u1, u2))
        return friendships
