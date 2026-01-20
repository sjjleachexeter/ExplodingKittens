const html5QrCode = new Html5Qrcode("reader");

function toggle_scanner_view() {
    const x = document.getElementById("scanner_view");

    if (x.style.display === "none") {
        x.style.display = "block";

        html5QrCode.start(
            {facingMode: "environment"},
            {
                fps: 10,
                qrbox: (viewfinderWidth, viewfinderHeight) => {
                    const width = viewfinderWidth * 0.9;
                    const height = viewfinderHeight * 0.9;
                    return {width, height};
                },

            },
            onScanSuccess,
        );
    } else {
        x.style.display = "none";
        html5QrCode.stop();
    }
}

function onScanSuccess(decodedText) {
    document.getElementById("result").innerText = decodedText;

    // Send to Django
    fetch("/scan/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify({barcode: decodedText})
    });
}

