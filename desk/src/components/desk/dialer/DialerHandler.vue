<template>
	<div>
		<div v-for="callLog in callLogs" :key="callLog">
			<Dialer
				:callLogId="callLog"
				@close-dialer="
					() => {
						callLogs.slice(callLogs.indexOf(callLog), 1)
					}
				"
			/>
		</div>
	</div>
</template>

<script>
import { inject, ref } from "vue"
import Dialer from "@/components/desk/dialer/Dialer.vue"

export default {
	name: "DialerHandler",
	setup() {
		const user = inject("user")
		const callLogs = ref([])
		return {
			user,
			callLogs,
		}
	},
	components: {
		Dialer,
	},
	mounted() {
		this.$resources.getOutgoingCall.fetch()
		this.$event.on("dialer:make-call", (options) => {
			if (this.dialerBusy) {
				this.$toast({
					title: "Call already in progress",
					customIcon: "circle-fail",
					appearance: "danger",
				})
				return
			}
			// this.makeCall(options)
			this.createDialer("CLOG-0000199-0000312")
		})
	},
	computed: {
		dialerBusy() {
			return this.callLogs.length > 0
		},
	},
	unmounted() {
		this.$event.off("dialer:make-call")
	},
	methods: {
		createDialer(callLogId) {
			this.callLogs.push(callLogId)
		},
	},
	resources: {
		makeCall() {
			return {
				method: "frappedesk.api.twilio.call",
				onSuccess: (callLogId) => {
					this.createDialer(callLogId)
				},
				onError: (err) => {
					this.$toast({
						title: "Something went wrong while making call",
						text: err,
						customIcon: "circle-fail",
						appearance: "danger",
					})
				},
			}
		},
		getOutgoingCall() {
			if (!(this.user && this.user.agent)) return
			return {
				method: "frappe.client.get_list",
				params: {
					doctype: "FD Twilio Call Log",
					filters: {
						reference_agent: this.user.agent.name,
						status: [
							"not in",
							[
								"completed",
								"busy",
								"no-answer",
								"canceled",
								"failed",
							],
						],
					},
					fields: ["name"],
				},
				onSuccess: (res) => {
					if (res.length) {
						this.createDialer(res[0].name)
					}
				},
			}
		},
	},
}
</script>
