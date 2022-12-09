<template>
	<div
		v-if="callLog && agent.doc"
		class="flex flex-col my-[16px] px-[8px] text-base"
	>
		<div class="flex flex-row justify-between">
			<div class="grow flex flex-col space-y-2">
				<div class="flex flex-row items-center space-x-2">
					<div class="p-1.5 rounded-[6px] h-fit">
						<FeatherIcon
							name="phone-outgoing"
							class="h-3 w-3 stroke-red-500"
						/>
					</div>
					<div class="font-medium text-base text-gray-900">
						{{ agent.doc.agent_name }}
					</div>
				</div>
				<div class="pl-[32px]">
					<div class="text-gray-500">{{ callLog.status }}</div>
				</div>
			</div>
			<div class="text-gray-500 font-normal text-[12px]">
				{{ $dayjs.longFormating($dayjs(callLog.creation).fromNow()) }}
			</div>
		</div>
	</div>
</template>

<script>
import { FeatherIcon } from "frappe-ui"

export default {
	name: "CallLogCard",
	props: ["callLog"],
	components: {
		FeatherIcon,
	},
	computed: {
		agent() {
			return this.$resources.agent
		},
	},
	resources: {
		agent() {
			return {
				type: "document",
				doctype: "Agent",
				name: this.callLog.reference_agent,
			}
		},
	},
}
</script>
