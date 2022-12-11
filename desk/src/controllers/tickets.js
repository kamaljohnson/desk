import { createDocumentResource, createResource } from "frappe-ui"
import { computed } from "vue"

function createTicketDocumentResource(ticketId, vm) {
	return createDocumentResource(
		{
			doctype: "Ticket",
			name: ticketId,
			debounce: 300,
			realtime: true,
		},
		vm
	)
}
function createTicketAssignmentsResource(ticketId, agentId) {
	return createResource({
		method: "frappedesk.api.ticket.assign_ticket_to_agent",
		params: {
			ticket_id: ticketId,
			agent_id: agentId,
		},
	})
}

function get(options, vm) {
	const ticketId = options?.ticketId
	const fieldname = options?.fieldname

	let resource = createTicketDocumentResource(ticketId, vm)
	if (!resource.doc) {
		resource.get.fetch()
	}
	let value = computed(() => {
		if (!resource.doc) return null
		return fieldname ? resource.doc[fieldname] : resource.doc
	})
	return value
}

function set(ticketId, fieldname, value) {
	if (fieldname === "_assign") {
		let resource = createTicketAssignmentsResource(ticketId, value)
		return resource.submit()
	}

	let resource = createTicketDocumentResource(ticketId)
	return resource.setValue.submit({ [fieldname]: value })
}

const tickets = {
	get,
	set,
}

export { tickets }
