<template>
	<div class="absolute bottom-11 right-0 m-4">
		<div class="w-[20rem] rounded-lg border bg-white p-3 shadow-md">
			<div v-if="callLog" class="flex flex-col space-y-3">
				<div
					class="flex flex-col w-full bg-gray-50 rounded-lg p-4 space-y-2"
				>
					<div
						v-if="contact"
						class="flex flex-col w-full items-center border-b py-4 space-y-2"
					>
						<Avatar size="lg" label="Contact Id" />
						<div class="flex flex-col space-y-0.5 items-center">
							<div>
								{{ callLog.reference_contact }}
							</div>
							<div class="text-base text-gray-500">
								{{ callLog.to }}
							</div>
						</div>
					</div>
					<router-link
						:to="{
							path: `/frappedesk/tickets/${callLog.reference_ticket}`,
						}"
					>
						<div
							class="flex flex-row items-center justify-between w-full text-base text-gray-600 hover:text-gray-900"
							role="button"
						>
							<div>
								{{ `Ticket: #${callLog.reference_ticket}` }}
							</div>
							<FeatherIcon
								name="arrow-up-right"
								class="h-4 w-4"
							/>
						</div>
					</router-link>
					<router-link
						:to="{
							path: `/frappedesk/contacts/${callLog.reference_contact}`,
						}"
					>
						<div
							class="flex flex-row items-center justify-between w-full text-base text-gray-600 hover:text-gray-900"
							role="button"
						>
							<div>
								{{ `Contact: ${callLog.reference_contact}` }}
							</div>
							<FeatherIcon
								name="arrow-up-right"
								class="h-4 w-4"
							/>
						</div>
					</router-link>
				</div>
				<div
					class="flex flex-row bg-gray-100 rounded-lg justify-between items-center p-2"
				>
					<div class="text-base italic text-gray-700 font-semibold">
						{{
							`${callLog.status
								.replace("-", " ")
								.toUpperCase()} ${
								callLog.status == "in-progress" &&
								callLog.call_started_at
									? callDuration
									: ""
							}`
						}}
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { Avatar, FeatherIcon } from "frappe-ui"

export default {
	name: "Dialer",
	props: ["callLogId"],
	components: {
		Avatar,
		FeatherIcon,
	},
	data() {
		return {
			callDuration: null,
		}
	},
	computed: {
		callLog() {
			const log = this.$resources.callLog.doc || null
			if (log) {
				if (log.call_started_at && !this.callDuration) {
					startCallDurationUpdateInterval(log.call_started_at)
				}
				if (this.callLogEndStatuses().includes(log.status)) {
					this.closeDialer()
				}
			}
			return log
		},
	},
	methods: {
		async closeDialer() {
			await new Promise((resolve) => setTimeout(resolve, 3000))
			this.$emit("close-dialer")
		},
		callLogEndStatuses() {
			return ["completed", "busy", "no-answer", "canceled", "failed"]
		},
		startCallDurationUpdateInterval(callStartedAt) {
			setInterval(() => {
				let nowTime = new Date(this.$dayjs())
				let startTime = new Date(this.$dayjs(callStartedAt))
				this.callDuration = this.$dayjs
					.duration(parseInt((nowTime - startTime) / 1000), "seconds")
					.format("H:m:s")
			}, 1000)
		},
	},
	resources: {
		callLog() {
			return {
				type: "document",
				doctype: "FD Twilio Call Log",
				name: this.callLogId,
			}
		},
	},
}
</script>
