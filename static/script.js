const cityInput = document.getElementById("cityInput");
const suggestions = document.getElementById("suggestions");

if (cityInput) {

    cityInput.addEventListener("input", async () => {

        let query = cityInput.value;

        if (query.length < 2) {
            suggestions.innerHTML = "";
            return;
        }

        let response = await fetch(`/search_city?q=${query}`);
        let data = await response.json();

        suggestions.innerHTML = "";

        data.forEach(city => {

            let div = document.createElement("div");

            div.innerText = `${city.name}, ${city.region}, ${city.country}`;

            div.onclick = () => {
                cityInput.value = city.name;
                suggestions.innerHTML = "";
            };

            suggestions.appendChild(div);
        });
    });
}

const voiceBtn = document.getElementById("voiceBtn");

if (voiceBtn) {

    voiceBtn.addEventListener("click", () => {

        const recognition =
        new(window.SpeechRecognition ||
            window.webkitSpeechRecognition)();

        recognition.lang = "en-US";

        recognition.start();

        recognition.onresult = function(event) {

            const city =
            event.results[0][0].transcript;

            cityInput.value = city;

        };

    });

}
function scrollDaily(amount){
    document.getElementById("dailySlider").scrollBy({
        left: amount,
        behavior: "smooth"
    });
}
