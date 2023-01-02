<template>
	<div>
		<slot id="form-body">
			<div v-for="field in fields" :key="field.fieldname">
				<TicketField
					:ticketId="ticketId"
					:fieldname="field.fieldname"
					:value="values[field.fieldname]"
					:editable="field.editable"
					@change="
						(val) => {
							updateFieldValue(field.fieldname, val)
						}
					"
				/>
			</div>
		</slot>
		<slot id="submit-action">
			<Button @click="save">Save</Button>
		</slot>
		<slot id="cancel-action"></slot>
	</div>
</template>

<script>
import { ref } from "vue"

export default {
	name: "TicketForm",
	props: ["ticketId", "isNew", "fields"],
	setup() {
		const formValues = ref({}) // {'subject': 'test', 'description': 'test''}
		const formErrors = ref({}) // {'subject': 'error in subject', 'description': 'error in description'}

		return {
			formValues,
			formErrors,
		}
	},
	computed: {
		ticket() {
			if (this.isNew) return
			return this.$resources.ticket.doc
		},
	},
	mounted() {
		this.formValues = this.getTicketInitialValues(
			this.isNew ? {} : this.ticket
		)
	},
	methods: {
		updateFieldValue(fieldname, value) {},
		validate() {},
		save() {},
		cancel() {},
		getTicketInitialValues(ticket = {}) {
			const values = {}
			this.fields.forEach((field) => {
				values[field.fieldname] =
					ticket[field.fieldname] || field.default || ""
			})
			return values
		},
	},
	resources: {
		ticket() {
			if (this.isNew) return
			return {
				type: "document",
				doctype: "Ticket",
				name: this.ticketId,
			}
		},
	},
}
</script>
