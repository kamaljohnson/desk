from werkzeug.wrappers import Response
import frappe
from twilio.twiml.voice_response import VoiceResponse, Dial
from frappedesk.utils import get_public_url
from frappedesk.handler.twilio import Twilio


@frappe.whitelist()
def call(contact_id, phone_number, agent_id, ticket_id):
	"""Make a call to the given phone number"""
	to = phone_number

	agent = frappe.get_doc("Agent", agent_id)
	if not agent:
		frappe.throw("Agent not found: {0}".format(agent_id))

	twilio_number = frappe.get_value("Agent Call Setting", agent_id, "twilio_number")
	if not twilio_number:
		frappe.throw("Twilio Number not found for agent: {0}".format(agent_id))

	from_ = frappe.get_value("User", agent.user, "phone")
	if not from_:
		frappe.throw("Phone Number not found for agent: {0}".format(agent_id))

	twilio = Twilio.connect()
	if not twilio:
		frappe.throw("Twilio not connected")

	call = twilio.call(
		to=to,
		from_=twilio_number,
		url=get_public_url("/api/method/frappedesk.api.twilio.outbound"),
	)

	call_log = frappe.get_doc(
		{
			"doctype": "FD Twilio Call Log",
			"call_sid": call.sid,
			"twilio_number": twilio_number,
			"to": to,
			"from_": from_,
			"status": "queued",
			"reference_contact": contact_id,
			"reference_agent": agent_id,
			"reference_ticket": ticket_id,
			"call_started_at": frappe.utils.now(),  # TODO: only set the call_started_at when the call log status is updated to in-progress
		}
	).insert()

	# update call logs via a hook to update the call log, refer: https://www.twilio.com/docs/voice/tutorials/how-to-retrieve-call-logs/python?code-sample=code-list-all-calls-example&code-language=Python&code-sdk-version=7.x#

	return call_log.name


@frappe.whitelist(allow_guest=True)
def outbound(**kwargs):
	args = frappe._dict(kwargs)

	twilio = Twilio.connect()
	if not twilio:
		return

	assert args.AccountSid == twilio.account_sid

	twilio_call_log = frappe.get_doc("FD Twilio Call Log", {"call_sid": args.CallSid})

	resp = VoiceResponse()

	resp.say(
		"This call may be recorded for quality assurance purposes.", voice="alice",
	)

	print("twilio_call_log", twilio_call_log)

	dial = Dial(
		caller_id=twilio_call_log.twilio_number,
		# record=self.settings.record_calls,
		# recording_status_callback=self.get_recording_status_callback_url(),
		# recording_status_callback_event='completed'
	)
	dial.number(
		twilio_call_log.from_,
		status_callback_event="initiated ringing answered completed",
		status_callback=get_public_url("/api/method/frappedesk.api.twilio.call_events"),
		status_callback_method="POST",
	)
	resp.append(dial)

	return Response(resp.to_xml(), mimetype="text/xml")


@frappe.whitelist(allow_guest=True)
def call_events(**kwargs):
	args = frappe._dict(kwargs)
	print("CALL EVENTS", args.ParentCallSid, args.CallStatus)

	twilio_call_log = frappe.get_doc(
		"FD Twilio Call Log", {"call_sid": args.ParentCallSid}
	)
	twilio_call_log.status = args.CallStatus
	twilio_call_log.save(ignore_permissions=True)

	return Response()
