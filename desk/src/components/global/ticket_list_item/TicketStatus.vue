<template>
	<Badge :color="color">{{ value }}</Badge>
</template>

<script>
export default {
	name: "TicketStatus",
	props: {
		value: {
			type: String,
			required: true,
		},
	},
	computed: {
		color() {
			return {
				Open: "red",
				Replied: "yellow",
				Resolved: "gray",
				Closed: "gray",
			}[this.value]
		},
	},
}
</script>
