#!/usr/bin/env python3
"""Receptionist agent with call transfer patterns.

Lab 2.8 Deliverable: Demonstrates department routing, time-based
transfers, and context passing to transferred calls.
"""

from datetime import datetime
from signalwire_agents import AgentBase, SwaigFunctionResult


class ReceptionistAgent(AgentBase):
    """Receptionist agent with intelligent call routing."""

    DEPARTMENTS = {
        "sales": {
            "number": "+15551111111",
            "description": "New purchases and pricing",
            "hours": (9, 18)
        },
        "support": {
            "number": "+15552222222",
            "description": "Technical assistance",
            "hours": (8, 20)
        },
        "billing": {
            "number": "+15553333333",
            "description": "Payments and invoices",
            "hours": (9, 17)
        },
        "returns": {
            "number": "+15554444444",
            "description": "Returns and exchanges",
            "hours": (10, 16)
        }
    }

    def __init__(self):
        super().__init__(name="receptionist")

        self.prompt_add_section(
            "Role",
            "You are the main receptionist. Help callers reach the right department."
        )

        self.prompt_add_section(
            "Departments",
            bullets=[
                f"{name.title()}: {info['description']}"
                for name, info in self.DEPARTMENTS.items()
            ]
        )

        self.prompt_add_section(
            "Guidelines",
            bullets=[
                "Always check if department is open before transferring",
                "Collect caller name and reason for context",
                "Offer alternatives if requested department is closed"
            ]
        )

        self.add_language("English", "en-US", "rime.spore")
        self._setup_functions()

    def _is_department_open(self, department: str) -> tuple:
        """Check if department is open. Returns (is_open, message)."""
        dept_info = self.DEPARTMENTS.get(department)
        if not dept_info:
            return False, "Unknown department"

        hour = datetime.now().hour
        start, end = dept_info["hours"]

        if start <= hour < end:
            return True, None
        else:
            return False, f"{department.title()} is open {start}:00 to {end}:00"

    def _setup_functions(self):
        """Define routing and transfer functions."""

        @self.tool(description="List all available departments")
        def list_departments() -> SwaigFunctionResult:
            dept_list = [
                f"{name.title()}: {info['description']}"
                for name, info in self.DEPARTMENTS.items()
            ]
            return SwaigFunctionResult("Our departments: " + "; ".join(dept_list))

        @self.tool(
            description="Check if a department is currently available",
            parameters={
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "Department name"
                    }
                },
                "required": ["department"]
            }
        )
        def check_availability(department: str) -> SwaigFunctionResult:
            department = department.lower()
            is_open, message = self._is_department_open(department)

            if is_open:
                dept_info = self.DEPARTMENTS.get(department)
                start, end = dept_info["hours"]
                return SwaigFunctionResult(
                    f"{department.title()} is open until {end}:00. "
                    "Would you like me to transfer you?"
                )
            return SwaigFunctionResult(message)

        @self.tool(
            description="Transfer to a department",
            parameters={
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "enum": list(self.DEPARTMENTS.keys()),
                        "description": "Department to transfer to"
                    }
                },
                "required": ["department"]
            }
        )
        def transfer_to_department(department: str) -> SwaigFunctionResult:
            department = department.lower()
            dept_info = self.DEPARTMENTS.get(department)

            if not dept_info:
                dept_list = ", ".join(self.DEPARTMENTS.keys())
                return SwaigFunctionResult(
                    f"Unknown department. Available: {dept_list}"
                )

            is_open, message = self._is_department_open(department)

            if not is_open:
                return SwaigFunctionResult(
                    f"I'm sorry, {message}. Would you like to leave a message "
                    "or try a different department?"
                )

            return (
                SwaigFunctionResult(f"Connecting you to {department} now.")
                .connect(dept_info["number"], final=True)
            )

        @self.tool(
            description="Transfer with caller context",
            parameters={
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "enum": list(self.DEPARTMENTS.keys()),
                        "description": "Department to transfer to"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for calling"
                    },
                    "caller_name": {
                        "type": "string",
                        "description": "Caller's name"
                    }
                },
                "required": ["department", "reason"]
            }
        )
        def transfer_with_context(
            department: str,
            reason: str,
            caller_name: str = None,
            raw_data: dict = None
        ) -> SwaigFunctionResult:
            department = department.lower()
            is_open, message = self._is_department_open(department)

            if not is_open:
                return SwaigFunctionResult(
                    f"Sorry, {message}. Would you like to leave a voicemail?"
                )

            dept_info = self.DEPARTMENTS[department]

            # Store context for receiving agent
            context = {
                "transfer_reason": reason,
                "caller_name": caller_name or "Unknown",
                "transfer_time": datetime.now().isoformat(),
                "from_receptionist": True
            }

            return (
                SwaigFunctionResult(
                    f"I'm transferring you to {department}. "
                    f"I'll let them know about your {reason}.",
                    post_process=True
                )
                .update_global_data(context)
                .connect(dept_info["number"], final=True)
            )

        @self.tool(
            description="Leave a voicemail for a closed department",
            parameters={
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "Department name"
                    },
                    "message": {
                        "type": "string",
                        "description": "Message to leave"
                    },
                    "callback_number": {
                        "type": "string",
                        "description": "Number to call back"
                    }
                },
                "required": ["department", "message"]
            }
        )
        def leave_voicemail(
            department: str,
            message: str,
            callback_number: str = None
        ) -> SwaigFunctionResult:
            return (
                SwaigFunctionResult(
                    f"Your message for {department} has been recorded. "
                    "They'll receive it when they open."
                )
                .update_global_data({
                    "voicemail_department": department,
                    "voicemail_message": message,
                    "voicemail_callback": callback_number,
                    "voicemail_time": datetime.now().isoformat()
                })
            )


if __name__ == "__main__":
    agent = ReceptionistAgent()
    agent.run()
