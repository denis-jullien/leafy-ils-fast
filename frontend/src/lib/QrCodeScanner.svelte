<!--https://www.reddit.com/r/sveltejs/comments/16vwawi/svelte_barcode_integration/-->

<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import {
		Html5QrcodeScanner,
		type Html5QrcodeResult,
		Html5QrcodeScanType,
		Html5QrcodeSupportedFormats,
		Html5QrcodeScannerState,
	} from 'html5-qrcode';

	export let width: number;
	export let height: number;
	export let paused: boolean = false;

	interface QrCodeScannerEvent {
		detect: { decodedText: string };
		error: { message: string };
	}
	const dispatch = createEventDispatcher<QrCodeScannerEvent>();

	function onScanSuccess(decodedText: string, decodedResult: Html5QrcodeResult): void {
		dispatch('detect', { decodedText });
	}

	// usually better to ignore and keep scanning
	function onScanFailure(message: string) {
		dispatch('error', { message });
	}

	let scanner: Html5QrcodeScanner;
	onMount(() => {
		scanner = new Html5QrcodeScanner(
			'qr-scanner',
			{
				fps: 10,
				qrbox: { width, height },
				aspectRatio: 1,
				supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA],
				formatsToSupport: [Html5QrcodeSupportedFormats.EAN_13],
			},
			false // non-verbose
		);
		scanner.render(onScanSuccess, onScanFailure);
	});

	// pause/resume scanner to avoid unintended scans
	$: togglePause(paused);
	function togglePause(paused: boolean): void {
		if (paused && scanner?.getState() === Html5QrcodeScannerState.SCANNING) {
			scanner?.pause();
		} else if (scanner?.getState() === Html5QrcodeScannerState.PAUSED) {
			scanner?.resume();
		}
	}
</script>

<div id="qr-scanner" class={$$props.class} />

<style>
    /* Hide unwanted icons */
    #qr-scanner :global(img[alt='Info icon']),
    #qr-scanner :global(img[alt='Camera based scan']) {
        display: none;
    }

    /* Change camera permission button text */
    #qr-scanner :global(#html5-qrcode-button-camera-permission) {
        visibility: hidden;
    }
    #qr-scanner :global(#html5-qrcode-button-camera-permission::after) {
        position: absolute;
        inset: auto 0 0;
        display: block;
        content: 'Allow camera access';
        visibility: visible;
        padding: 10px 0;
    }
</style>

<!--<script lang="ts">-->
<!--	import { onMount } from 'svelte';-->
<!--	import {-->
<!--		Html5QrcodeScanner,-->
<!--		type Html5QrcodeResult,-->
<!--		Html5QrcodeScanType,-->
<!--		Html5QrcodeSupportedFormats,-->
<!--		Html5QrcodeScannerState,-->
<!--	} from 'html5-qrcode';-->

<!--	let { scanSuccess, scanFailure, class: klass, width, height, paused = false } = $props();-->

<!--	let scanner: Html5QrcodeScanner;-->
<!--	onMount(() => {-->
<!--		scanner = new Html5QrcodeScanner(-->
<!--			'qr-scanner',-->
<!--			{-->
<!--				fps: 10,-->
<!--				qrbox: { width, height },-->
<!--				aspectRatio: 1,-->
<!--				supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA],-->
<!--				formatsToSupport: [Html5QrcodeSupportedFormats.QR_CODE],-->
<!--			},-->
<!--			false // non-verbose-->
<!--		);-->
<!--		scanner.render(scanSuccess, scanFailure);-->
<!--	});-->

<!--	// pause/resume scanner to avoid unintended scans-->

<!--	let togglePause = $derived.by((paused) => {-->
<!--		if (paused && scanner?.getState() === Html5QrcodeScannerState.SCANNING) {-->
<!--			scanner?.pause();-->
<!--		} else if (scanner?.getState() === Html5QrcodeScannerState.PAUSED) {-->
<!--			scanner?.resume();-->
<!--		}-->
<!--	})-->
<!--</script>-->

<!--<div id="qr-scanner" class={klass} />-->

<!--<style>-->
<!--    /* Hide unwanted icons */-->
<!--    #qr-scanner :global(img[alt='Info icon']),-->
<!--    #qr-scanner :global(img[alt='Camera based scan']) {-->
<!--        display: none;-->
<!--    }-->

<!--    /* Change camera permission button text */-->
<!--    #qr-scanner :global(#html5-qrcode-button-camera-permission) {-->
<!--        visibility: hidden;-->
<!--    }-->
<!--    #qr-scanner :global(#html5-qrcode-button-camera-permission::after) {-->
<!--        position: absolute;-->
<!--        inset: auto 0 0;-->
<!--        display: block;-->
<!--        content: 'Allow camera access';-->
<!--        visibility: visible;-->
<!--        padding: 10px 0;-->
<!--    }-->
<!--</style>-->