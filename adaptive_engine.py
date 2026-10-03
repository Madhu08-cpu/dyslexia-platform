class AdaptiveEngine:
    def __init__(self):
        # Thresholds for triggering adaptation
        self.accuracy_threshold = 70.0  # Percentage
        self.frustration_states = ["Frustrated", "Strained", "Confused"]

    def evaluate_adaptation_triggers(self, current_accuracy, detected_emotion):
        """
        Evaluates real-time metrics to determine if the reading interface 
        needs to dynamically adjust difficulty or styling.
        """
        needs_adaptation = False
        adjustment_action = "Maintain Normal Pacing"

        # Trigger 1: Low accuracy combined with high stress/frustration
        if current_accuracy < self.accuracy_threshold or detected_emotion in self.frustration_states:
            needs_adaptation = True
            adjustment_action = "Decrease reading speed, increase line spacing, and simplify vocabulary."
        
        # Trigger 2: High accuracy and steady state
        elif current_accuracy >= 90.0 and detected_emotion == "Focused":
            needs_adaptation = True
            adjustment_action = "Slightly increase complexity or introduce a bonus challenge."

        return {
            "trigger": needs_adaptation,
            "action": adjustment_action
        }