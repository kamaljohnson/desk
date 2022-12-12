<template>
	<div
		v-if="callLog && agent"
		class="flex flex-col my-[16px] px-[8px] text-base bg-red-50 py-2 rounded-[6px]"
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
					<div class="flex flex-row space-x-3 items-center">
						<div
							class="font-medium text-base text-gray-900 flex flex-row space-x-2 items-center"
						>
							<div>
								{{ agent.agent_name }}
							</div>
							<FeatherIcon name="arrow-right" class="h-3" />
							<div>
								{{ contact.first_name }}
							</div>
						</div>
						<div class="text-gray-500 font-normal">
							({{ callLog.status }})
						</div>
					</div>
				</div>
			</div>
			<div class="text-gray-500 font-normal text-[12px]">
				{{ $dayjs.longFormating($dayjs(callLog.creation).fromNow()) }}
			</div>
		</div>
		<div class="flex flex-row space-x-1 items-center ml-[20px]">
			<audio v-if="callLog.recording_url" controls>
				<source :src="callLog.recording_url" type="audio/ogg" />
			</audio>
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
			return this.$resources.agent.doc || null
		},
		contact() {
			return this.$resources.contact.doc || null
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
		contact() {
			return {
				type: "document",
				doctype: "Contact",
				name: this.callLog.reference_contact,
			}
		},
	},
}
</script>

<style>
audio {
	/*border-radius: 90px;*/
	width: 100%;
	height: 35px;
}

audio::-webkit-media-controls-mute-button {
	display: none !important;
}

audio::-webkit-media-controls-volume-slider {
	display: none !important;
}

audio::-webkit-media-controls-volume-control-container.closed {
	display: none !important;
}
audio::-webkit-media-controls-volume-control-container {
	display: none !important;
}
audio::-webkit-media-controls-panel {
	background: rgb(254, 242, 242);
	padding: 0px;
}
</style>
