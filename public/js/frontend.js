const socket = io()

socket.on('result', (img) => {
    const image = new Blob([img], { type: 'image/png' });
    const imageUrl = URL.createObjectURL(image);

    document.querySelector('#waitFlag').innerHTML = ""

    document.querySelector('#photoResult').setAttribute("src", imageUrl);

    document.querySelector('#downloadButton').innerHTML = 
        `<a href="${imageUrl}" download style="position: absolute; top: 310px; left: 850px;"><button>Download</button></a>`
})

document.querySelector('#imgForm').addEventListener('submit', (event) => {
    event.preventDefault()
    var img = document.querySelector('#fileInput').files[0]
    const reader = new FileReader();
    reader.onloadend = function() {
        const image = new Blob([img], { type: 'image/png' });
        const imageUrl = URL.createObjectURL(image);
        document.querySelector('#photoLoad').setAttribute("src", imageUrl);
    }
    reader.readAsArrayBuffer(img);

    document.querySelector('#inputType').innerHTML = `<button id="UQ" style="position: absolute; top: 20px; left: 340px; width: 170px;">Uniform quantization</button>
      <button id="MC" style="position: absolute; top: 50px; left: 340px; width: 170px;">Median cut</button>
      <button id="KM" style="position: absolute; top: 80px; left: 340px; width: 170px;">K-Means</button>
      <button id="VQ" style="position: absolute; top: 110px; left: 340px; width: 170px;">Vector quantization</button>
      <button id="OCT" style="position: absolute; top: 140px; left: 340px; width: 170px;">OCTree</button>
      <button id="AC" style="position: absolute; top: 170px; left: 340px; width: 170px;">Aglomerative clustering</button>
      <button id="PM" style="position: absolute; top: 200px; left: 340px; width: 170px;">P-medians</button>
      <button id="SRCNN" style="position: absolute; top: 230px; left: 340px; width: 170px;">SRCNN</button>`
})

document.querySelector('#inputType').addEventListener('click', (
  event) => {
    if (event.target.id != "Proceed") type = event.target.id
    
    field = document.querySelector('#inputParam')
    info = document.querySelector('#Info')

    switch(event.target.id) {
        case "UQ":
            field.innerHTML = `<h4 style="position: absolute; top: 10px;">Uniform quantization</h4>
                <p style="position: absolute; top: 50px;">Number of regions</p>
                <input id="UQ_r" type="number" value="2" min="2" max="16" style="position: absolute; top: 90px;"/>`
            info.innerHTML = `<h3>Uniform quantization</h3>
                <p>Algorithm for quantization with range of colors split.</p>
                <p>Require number of regions for color in range from 2 to 16.</p>`
            break;
        case "MC":
            field.innerHTML = `<h4 style="position: absolute; top: 10px;">Median cut</h4>
                <p style="position: absolute; top: 50px;">Depth</p>
                <input id="MC_d" type="number" value="2" min="1" max="8" style="position: absolute; top: 90px;"/>`
            info.innerHTML = `<h3>Median cut</h3>
                <p>Quantization with split on median in color with bigest variety.</p>
                <p>Require depth, which show how many splits will be produced.</p>
                <p>Result colors will be 2^depth, so enter integer from 1 to 8.</p>`
            break;
        case "KM":
            field.innerHTML = `<h4 style="position: absolute; top: 10px;">K-means</h4>
                <p style="position: absolute; top: 50px;">Number of cluster</p>
                <input id="KM_c" type="number" value="2" min="2" max="32" style="position: absolute; top: 90px;"/>
                <p style="position: absolute; top: 110px;">Max iteration</p>
                <input id="KM_i" type="number" value="1" min="1" max="20" style="position: absolute; top: 150px;"/>`
            info.innerHTML = `<h3>K-means</h3>
                <p>Quantization with k-means clustering.</p>
                <p>Number of cluster give amount of result colors. Enter integer from 2 to 32.</p>
                <p>Max iteration show maximum number of repeat. Enter integer from 1 to 20.</p>`
            break;
        case "VQ":
            field.innerHTML = `<h4 style="position: absolute; top: 10px;">Vector quantization</h4>
                <p style="position: absolute; top: 50px;">Codebook</p>
                <input id="VQ_c" type="number" value="4" min="1" max="64" style="position: absolute; top: 90px;"/>
                <p style="position: absolute; top: 110px;">Epsilon</p>
                <input id="VQ_e" type="number" value="0.05" min="0.01" max="1" style="position: absolute; top: 150px;"/>
                <p style="position: absolute; top: 170px;">Block width</p>
                <input id="VQ_w" type="number" value="2" min="1" max="64" style="position: absolute; top: 210px;"/>
                <p style="position: absolute; top: 230px;">Block height</p>
                <input id="VQ_h" type="number" value="2" min="1" max="64" style="position: absolute; top: 270px;"/>`
            info.innerHTML = `<h3>Vector quantization</h3>
                <p>This algorithm perform block quantization.</p>
                <p>Codebook size give result colors as nearest bigger power of two. Enter integer from 1 to 64.</p>
                <p>Epsilon as threshold. Send positive float less than 1.</p>
                <p>Block parameters show how big is sliding window, must be from 1 to 64.</p>`
            break;
        case "OCT":
            field.innerHTML = `<h4 style="position: absolute; top: 10px;">OCTree</h4>
                <p style="position: absolute; top: 50px;">Pallete</p>
                <input id="OCT_p" type="number" value="16" min="8" max="128" style="position: absolute; top: 90px;"/>`
            info.innerHTML = `<h3>OCTree</h3>
                <p>Quantization with graph trees.</p>
                <p>Palette give amount of result colors. Enter integer from 8 to 128.</p>`
            break;
        case "AC":
            field.innerHTML = `<h4 style="position: absolute; top: 10px;">Aglomerative clustering</h4>
                <p style="position: absolute; top: 50px;">Number of colors</p>
                <input id="AC_c" type="number" value="16" min="2" max="64" style="position: absolute; top: 90px;"/>`
            info.innerHTML = `<h3>Aglomerative clustering</h3>
                <p>Image compression with closest colors combining.</p>
                <p>Nuvber of colors show result amount. Enter integer from 2 to 64.</p>`
            break;
        case "PM":
            field.innerHTML = `<h4 style="position: absolute; top: 10px;">P-Medians</h4>
                <p style="position: absolute; top: 50px;">Number of colors</p>
                <input id="PM_c" type="number" value="2" min="2" max="16" style="position: absolute; top: 90px;"/>`
            info.innerHTML = `<h3>P-Medians</h3>
                <p>Image compression using optimization.</p>
                <p>Nuvber of colors show result amount. Enter integer from 2 to 16.</p>`
            break;
        case "SRCNN":
            field.innerHTML = `<h4 style="position: absolute; top: 10px;">SRCNN</h4>`
            info.innerHTML = `<h3>Super resolution convolutional neural network</h3>
                <p>Image enchantment using neural network.</p>`
            break;
    }

    document.querySelector('#photoResult').removeAttribute("src");

    document.querySelector('#downloadButton').innerHTML = ""

    if (!document.querySelector('#Proceed')) {
        document.querySelector('#inputType').innerHTML += 
            `<button id="Proceed" style="position: absolute; top: 280px; left: 340px; width: 170px;">Proceed</button>`

        document.querySelector('#Proceed').addEventListener('click', () => {
            var img = document.querySelector('#fileInput').files[0]

            switch(type) {
                case "UQ":
                    var UQ_r = document.querySelector('#UQ_r').value

                    socket.emit(type,  {
                        img: img,
                        UQ_r: clamp(UQ_r, 2, 16)
                    })

                    break;
                case "MC":
                    var MC_d = document.querySelector('#MC_d').value

                    socket.emit(type,  {
                        img: img,
                        MC_d: clamp(MC_d, 1, 8)
                    })

                    break;
                case "KM":
                    var KM_c = document.querySelector('#KM_c').value
                    var KM_i = document.querySelector('#KM_i').value

                    socket.emit(type,  {
                        img: img,
                        KM_c: clamp(KM_c, 2, 32),
                        KM_i: clamp(KM_i, 1, 20)
                    })

                    break;
                case "VQ":
                    var VQ_c = document.querySelector('#VQ_c').value
                    var VQ_e = document.querySelector('#VQ_e').value
                    var VQ_w = document.querySelector('#VQ_w').value
                    var VQ_h = document.querySelector('#VQ_h').value

                    socket.emit(type,  {
                        img: img,
                        VQ_c: clamp(VQ_c, 1, 64),
                        VQ_e: clamp(VQ_e, 0.01, 1),
                        VQ_w: clamp(VQ_w, 1, 64),
                        VQ_h: clamp(VQ_h, 1, 64)
                    })
                    break;
                case "OCT":
                    var OCT_p = document.querySelector('#OCT_p').value

                    socket.emit(type,  {
                        img: img,
                        OCT_p: clamp(OCT_p, 8, 128)
                    })
                    break;
                case "AC":
                    var AC_c = document.querySelector('#AC_c').value

                    socket.emit(type,  {
                        img: img,
                        AC_c: clamp(AC_c, 2, 64)
                    })
                    break;
                case "PM":
                    var PM_c = document.querySelector('#PM_c').value

                    socket.emit(type,  {
                        img: img,
                        PM_c: clamp(PM_c, 2, 16)
                    })
                    break;
                case "SRCNN":
                    socket.emit(type,  {
                        img: img
                    })

                    break;
            }

            document.querySelector('#waitFlag').innerHTML = 
                `<h1 style="position: absolute; top: 100px; left: 835px;">Waiting</h1>`
        })
    }
})

function clamp(num, min, max) {
  return num <= min 
    ? min 
    : num >= max 
      ? max 
      : num
}