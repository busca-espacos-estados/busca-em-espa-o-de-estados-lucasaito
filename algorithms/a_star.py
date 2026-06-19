import heapq
import itertools
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = index // 3, index % 3
            goal_index = GOAL_STATE.index(tile)
            goal_row, goal_col = goal_index // 3, goal_index % 3
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        counter = itertools.count()     
        start_f = self.heuristic(initial)
        frontier = [(start_f, next(counter), initial)]
        best_cost = {initial: 0}       

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            f, _, node = heapq.heappop(frontier)

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            if node.cost > best_cost.get(node, float("inf")):
                continue

            nodes_expanded += 1

            for child in node.neighbors():
                nodes_generated += 1
                if child.cost < best_cost.get(child, float("inf")):
                    best_cost[child] = child.cost
                    child_f = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (child_f, next(counter), child))

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )