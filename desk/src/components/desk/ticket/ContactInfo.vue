<template>
	<div v-if="contact" class="space-y-[12px]">
		<div class="flex flex-row items-center space-x-[12px]">
			<CustomAvatar
				:label="contactFullName"
				:imageURL="contact?.image"
				size="md"
				class="ml-[-6.5px]"
			/>
			<a
				:title="contactFullName"
				class="grow truncate font-normal text-base"
				>{{ contactFullName }}</a
			>
		</div>
		<div
			v-if="contact.phone_nos.length > 0"
			class="flex space-x-[12px] items-center"
		>
			<FeatherIcon
				name="phone"
				class="stroke-gray-500"
				style="width: 15px"
			/>
			<div
				class="space-y-1"
				v-for="phone_no in contact.phone_nos"
				:key="phone_no"
			>
				<a :title="phone_no.phone" class="text-gray-700 text-base">
					{{ phone_no.phone }}
				</a>
			</div>
			<div
				v-if="twilioSettings?.enabled && user.agent"
				class="bg-blue-500 text-white px-2 py-0.5 rounded-md shadow-sm hover:shadow-md"
				role="button"
				@click="
					() => {
						$event.emit('dialer:make-call', {
							contact_id: contact.name,
							phone_number: phone_no.phone,
							agent_id: user.agent.name,
							ticket_id: ticket.name,
						})
					}
				"
			>
				Call
			</div>
		</div>
		<div v-if="contact.email_ids.length > 0" class="flex space-x-[12px]">
			<FeatherIcon
				name="mail"
				class="stroke-gray-500 mt-[2.5px]"
				style="width: 15px; height: 15px"
			/>
			<div
				class="space-y-1 max-w-[173px] break-words"
				v-for="email in contact.email_ids"
				:key="email"
			>
				<div :title="email.email_id" class="text-gray-700 text-base">
					<a :title="email.email_id">{{ email.email_id }}</a>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { FeatherIcon } from "frappe-ui"
import CustomAvatar from "@/components/global/CustomAvatar.vue"
import { inject } from "vue"

export default {
	name: "ContactInfo",
	props: ["contactId"],
	components: {
		FeatherIcon,
		CustomAvatar,
	},
	setup() {
		const user = inject("user")

		return {
			user,
		}
	},
	computed: {
		contact() {
			return this.$resources.contact.doc || null
		},
		twilioSettings() {
			return this.$resources.twilioSettings.doc || null
		},
		contactFullName() {
			if (this.contact) {
				return (
					(this.contact.first_name || "") +
					" " +
					(this.contact.last_name || "")
				).slice(0, 40)
			}
		},
	},
	resources: {
		contact() {
			return {
				type: "document",
				doctype: "Contact",
				name: this.contactId,
			}
		},
		twilioSettings() {
			return {
				type: "document",
				doctype: "Twilio Settings",
				name: "Twilio Settings",
			}
		},
	},
}
</script>
