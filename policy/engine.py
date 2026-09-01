from core.interfaces import Capability, PolicyDecision


class PolicyEngine:

    def evaluate(self, tool, context=None):

        capability = self._get_capability(tool)

        if capability is None:
            return PolicyDecision(
                decision="deny",
                reason="unknown capability",
                requires_confirmation=False,
            )

        if capability == Capability.READ_ONLY:
            return PolicyDecision(
                decision="allow",
                reason="read_only tools are permitted",
                requires_confirmation=False,
            )

        if capability == Capability.STATE_CHANGING:
            return PolicyDecision(
                decision="confirm",
                reason="state_changing tools require confirmation",
                requires_confirmation=True,
            )

        if capability == Capability.DESTRUCTIVE:
            return PolicyDecision(
                decision="deny",
                reason="destructive tools are not permitted by default",
                requires_confirmation=False,
            )

        return PolicyDecision(
            decision="deny",
            reason="unsupported capability",
            requires_confirmation=False,
        )

    def _get_capability(self, tool):

        if hasattr(tool, "capability"):
            capability = tool.capability

            if isinstance(capability, Capability):
                return capability

            if isinstance(capability, str) and capability in Capability._value2member_map_:
                return Capability(capability)

        return None
