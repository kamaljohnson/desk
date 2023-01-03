<template>
	<div class="flex flex-col space-y-2">
		<div class="flex flex-col space-y-2">
			<div v-for="field in fields" :key="field.fieldname">
				<TicketField
					:ticketId="ticketId"
					:fieldname="field.fieldname"
					:value="values[field.fieldname]"
					:editable="field.editable || false"
					@change="
						(val) => {
							if (!editing) {
								editing = true
								tempValues = { ...ticket }
							}
							tempValues[field.fieldname] = val
						}
					"
				/>
			</div>
		</div>
		<div class="flex flex-row-reverse w-full">
			<div v-if="editing" class="flex flex-row space-x-2">
				<Button @click="cancel"> Cancel </Button>
				<Button
					appearance="primary"
					@click="
						() => {
							if (validate()) {
								save()
							}
						}
					"
				>
					Save
				</Button>
			</div>
		</div>
	</div>
</template>

<script>
import { ref } from "vue"
import TicketField from "@/components/global/TicketField.vue"

export default {
	name: "TicketForm",
	props: ["ticketId", "fields"],
	components: {
		TicketField,
	},
	setup() {
		const editing = ref(false)
		const tempValues = ref({})
		const errors = ref({})

		return {
			editing,
			tempValues,
			errors,
		}
	},
	computed: {
		ticket() {
			return this.$resources.ticket.doc
		},
		values() {
			if (this.editing) {
				return this.tempValues
			} else {
				return this.ticket
			}
		},
	},
	methods: {
		validate() {
			return true
		},
		save() {
			console.log("save")
		},
		cancel() {
			this.editing = false
		},
	},
	resources: {
		ticket() {
			return {
				type: "document",
				doctype: "Ticket",
				name: this.ticketId,
			}
		},
	},
}
</script>
