"""
Message Templates for Voice Conversations.
Provides dynamic templates for different scenarios and tones.
"""

from typing import Dict, Any
from string import Template


class MessageTemplates:
    """
    Message template manager for voice conversations.
    Supports multiple tones and scenarios with dynamic placeholders.
    """
    
    # Predicted Failure Warning - Gentle Tone
    PREDICTED_FAILURE_GENTLE = {
        "greeting": Template("🔮 Namaste ${owner_name}, this is Aurora - your vehicle's guardian angel and predictive maintenance wizard!"),
        "issue": Template(
            "We've detected some early signs of ${component} wear in your ${vehicle_model}. "
            "Our AI analysis shows a ${probability}% probability of potential issues developing "
            "within the next ${timeframe}."
        ),
        "explanation": Template(
            "This is based on continuous monitoring of your vehicle's telematics data. "
            "The good news is we caught this early, so we can prevent any major problems."
        ),
        "recommendation": Template(
            "We recommend scheduling an inspection at your earliest convenience. "
            "This is a ${risk_level} priority situation, and addressing it now will help avoid "
            "more costly repairs later."
        ),
        "offer": Template(
            "We've found an available slot at ${workshop_name} on ${recommended_slot}. "
            "Would this work for you?"
        ),
        "closing": Template(
            "We're here to keep your vehicle running smoothly. "
            "Can I go ahead and book this appointment for you?"
        )
    }
    
    # Predicted Failure Warning - Urgent Tone
    PREDICTED_FAILURE_URGENT = {
        "greeting": Template("🚨 RED ALERT! ${owner_name}, this is Aurora with a critical message about your ${vehicle_model}."),
        "issue": Template(
            "We've detected a critical ${component} issue that requires immediate attention. "
            "Our AI predicts a ${probability}% chance of failure within ${timeframe}."
        ),
        "risk": Template(
            "This is a ${risk_level} priority alert. Continuing to drive may be unsafe and "
            "could lead to complete ${component} failure."
        ),
        "recommendation": Template(
            "We strongly recommend you stop driving and schedule immediate service. "
            "Your safety is our top priority."
        ),
        "offer": Template(
            "We have an emergency slot available at ${workshop_name} ${recommended_slot}. "
            "This is the earliest available appointment."
        ),
        "closing": Template(
            "Shall I book this emergency service appointment for you right away?"
        )
    }
    
    # Appointment Reminder
    APPOINTMENT_REMINDER = {
        "greeting": Template("⏰ Hi ${owner_name}! Aurora here - your friendly neighborhood reminder bot!"),
        "reminder": Template(
            "Your ${vehicle_model} is scheduled for ${service_type} at ${workshop_name} "
            "on ${appointment_date} at ${appointment_time}."
        ),
        "preparation": Template(
            "The estimated service time is ${duration} minutes. "
            "Please bring your vehicle registration and any relevant documents."
        ),
        "confirmation": Template(
            "Can you confirm you'll be able to make this appointment?"
        ),
        "closing": Template(
            "Great! We'll see you ${appointment_date}. If anything changes, "
            "please call us at ${workshop_phone}."
        )
    }
    
    # Declined Appointment Recovery
    BOOKING_RECOVERY = {
        "greeting": Template("🎯 Hi ${owner_name}! Aurora again - I noticed the ${original_slot} didn't work out. No worries, life happens!"),
        "empathy": Template(
            "I completely understand scheduling can be challenging. "
            "Let me help you find a more convenient time."
        ),
        "importance": Template(
            "Given the ${risk_level} priority of your ${component} issue, "
            "it's important we get this addressed within ${timeframe}."
        ),
        "alternatives": Template(
            "I have several alternative slots available: "
            "${alternate_slots}. "
            "Would any of these work better for your schedule?"
        ),
        "flexibility": Template(
            "We can also arrange for a pickup service if that would be more convenient. "
            "Or we can schedule an evening or weekend appointment."
        ),
        "closing": Template(
            "What would work best for you? I'm here to make this as easy as possible."
        )
    }
    
    # Post-Service Feedback
    POST_SERVICE_FEEDBACK = {
        "greeting": Template("⭐ Hello ${owner_name}! Aurora here, doing my quality check rounds!"),
        "service_recap": Template(
            "Your ${vehicle_model} was serviced at ${workshop_name} on ${service_date} "
            "for ${service_type}."
        ),
        "satisfaction": Template(
            "On a scale of 1 to 5, how satisfied are you with the service you received?"
        ),
        "issue_resolution": Template(
            "Has the ${component} issue been completely resolved? "
            "Are you experiencing any remaining concerns?"
        ),
        "prediction_accuracy": Template(
            "Our AI predicted a ${component} issue, and the service confirmed ${actual_finding}. "
            "This helps us improve our prediction accuracy."
        ),
        "closing": Template(
            "Thank you for your feedback. We're continuously improving our service. "
            "Is there anything else I can help you with today?"
        )
    }
    
    # Safety Check Question
    SAFETY_CHECK = {
        "question": Template("Is it safe to drive?"),
        "low_risk": Template(
            "Based on our analysis, your vehicle is currently safe to drive for short distances. "
            "However, we recommend scheduling service within ${timeframe} to prevent the issue from worsening."
        ),
        "medium_risk": Template(
            "You can drive to the service center, but we recommend avoiding long trips or highway driving. "
            "The ${component} issue could worsen with extended use."
        ),
        "high_risk": Template(
            "We strongly advise against driving. The ${component} failure risk is ${probability}%, "
            "which could lead to a breakdown or safety hazard. "
            "We recommend arranging a tow or pickup service."
        )
    }
    
    # Cost Inquiry
    COST_INQUIRY = {
        "question": Template("How much will this cost?"),
        "estimate": Template(
            "Based on the ${component} issue, the estimated cost is between ${cost_min} and ${cost_max} rupees. "
            "This includes parts and labor."
        ),
        "breakdown": Template(
            "The cost breakdown is: Parts ${parts_cost} rupees, Labor ${labor_cost} rupees, "
            "and diagnostic fee ${diagnostic_cost} rupees."
        ),
        "savings": Template(
            "By addressing this now, you're saving approximately ${savings} rupees "
            "compared to waiting until complete failure."
        ),
        "warranty": Template(
            "All repairs come with a ${warranty_period} warranty. "
            "We also offer flexible payment options if needed."
        )
    }
    
    # Alternate Slot Offer
    ALTERNATE_SLOTS = {
        "morning": Template("Tomorrow morning at 9 AM"),
        "afternoon": Template("Tomorrow afternoon at 2 PM"),
        "evening": Template("This evening at 6 PM"),
        "weekend": Template("This Saturday at 10 AM"),
        "next_week": Template("Next Monday at 11 AM")
    }
    
    @classmethod
    def get_template(cls, scenario: str, tone: str = "gentle") -> Dict[str, Template]:
        """
        Get message template for a scenario.
        
        Args:
            scenario: Scenario name (e.g., "predicted_failure", "appointment_reminder")
            tone: Tone to use ("gentle", "urgent", "friendly", "technical")
        
        Returns:
            Dictionary of message templates
        """
        scenario_map = {
            "predicted_failure": {
                "gentle": cls.PREDICTED_FAILURE_GENTLE,
                "urgent": cls.PREDICTED_FAILURE_URGENT
            },
            "appointment_reminder": {
                "gentle": cls.APPOINTMENT_REMINDER,
                "friendly": cls.APPOINTMENT_REMINDER
            },
            "booking_recovery": {
                "gentle": cls.BOOKING_RECOVERY,
                "friendly": cls.BOOKING_RECOVERY
            },
            "post_service_feedback": {
                "gentle": cls.POST_SERVICE_FEEDBACK,
                "friendly": cls.POST_SERVICE_FEEDBACK
            },
            "safety_check": {
                "technical": cls.SAFETY_CHECK
            },
            "cost_inquiry": {
                "technical": cls.COST_INQUIRY
            }
        }
        
        scenario_templates = scenario_map.get(scenario, {})
        return scenario_templates.get(tone, scenario_templates.get("gentle", {}))
    
    @classmethod
    def render_template(cls, template_dict: Dict[str, Template], context: Dict[str, Any]) -> Dict[str, str]:
        """
        Render templates with context data.
        
        Args:
            template_dict: Dictionary of templates
            context: Context data for placeholders
        
        Returns:
            Dictionary of rendered messages
        """
        rendered = {}
        for key, template in template_dict.items():
            try:
                rendered[key] = template.safe_substitute(context)
            except Exception as e:
                rendered[key] = f"[Template error: {e}]"
        
        return rendered
    
    @classmethod
    def build_full_message(cls, scenario: str, tone: str, context: Dict[str, Any]) -> str:
        """
        Build a complete message from templates.
        
        Args:
            scenario: Scenario name
            tone: Tone to use
            context: Context data
        
        Returns:
            Complete message string
        """
        templates = cls.get_template(scenario, tone)
        rendered = cls.render_template(templates, context)
        
        # Join all parts with appropriate spacing
        message_parts = []
        for key in templates.keys():
            if key in rendered:
                message_parts.append(rendered[key])
        
        return " ".join(message_parts)
