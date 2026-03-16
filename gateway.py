class Gateway:
    def __init__(self, primaryBreaker: CircuitBreaker, secondaryBreaker: CircuitBreaker):
        self.primary = primaryBreaker
        self.secondary = secondaryBreaker

    def routeRequests(self, totalRequests: int) -> List[str]:
        ans = []

        for requestId in range(totalRequests):
            primary_attempted = False
            secondary_attempted = False

            # First try primary if closed
            if self.primary.can_attempt():
                primary_attempted = True
                primary_success = self.primary.attempt(requestId)

                # If primary fails, try secondary if closed
                if not primary_success:
                    if self.secondary.can_attempt():
                        secondary_attempted = True
                        self.secondary.attempt(requestId)
                    else:
                        self.secondary.on_blocked()
            else:
                self.primary.on_blocked()

                # Primary open -> route directly to secondary
                if self.secondary.can_attempt():
                    secondary_attempted = True
                    self.secondary.attempt(requestId)
                else:
                    self.secondary.on_blocked()

            # Build routing string
            if primary_attempted and secondary_attempted:
                ans.append("Primary -> Secondary")
            elif primary_attempted:
                ans.append("Primary")
            elif secondary_attempted:
                ans.append("Secondary")
            else:
                ans.append("Rejected")

        return ans