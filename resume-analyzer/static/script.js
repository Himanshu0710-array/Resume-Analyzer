document.getElementById("form").addEventListener("submit", function(e) {
    e.preventDefault();

    let formData = new FormData(this);
    let submitBtn = document.getElementById("submitBtn");
    let loading = document.getElementById("loading");
    let result = document.getElementById("result");
    
    let shortlistedContainer = document.getElementById("shortlisted-container");
    let otherContainer = document.getElementById("other-container");
    let noShortlisted = document.getElementById("no-shortlisted");

    // Show loading state
    submitBtn.disabled = true;
    loading.style.display = "block";
    result.style.display = "none";
    shortlistedContainer.innerHTML = "";
    otherContainer.innerHTML = "";
    noShortlisted.style.display = "none";

    fetch("/analyze", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        // Hide loading state
        submitBtn.disabled = false;
        loading.style.display = "none";
        result.style.display = "block";

        let resultsArray = data.results;
        
        let hasShortlisted = false;
        let template = document.getElementById("candidate-template");

        if (resultsArray.length === 0) {
            noShortlisted.style.display = "block";
            document.getElementById("other-section").style.display = "none";
            return;
        }
        
        document.getElementById("other-section").style.display = "block";

        resultsArray.forEach((candidate, index) => {
            let clone = template.content.cloneNode(true);
            
            let card = clone.querySelector(".candidate-card");
            card.style.animationDelay = `${index * 0.1}s`;

            clone.querySelector(".filename").textContent = candidate.filename;
            
            let score = candidate.score;
            clone.querySelector(".percentage").textContent = score + "%";
            
            let circle = clone.querySelector(".circle");
            // Set slight delay for stroke dasharray to trigger transition
            setTimeout(() => {
                circle.setAttribute('stroke-dasharray', `${score}, 100`);
            }, 50);

            if(score >= 80) {
                circle.style.stroke = "#2ed573";
            } else if(score >= 65) {
                circle.style.stroke = "#00f2fe"; // bright blue for 65+
            } else if(score >= 50) {
                circle.style.stroke = "#ffa502";
            } else {
                circle.style.stroke = "#ff4757";
            }

            let matchedContainer = clone.querySelector(".matched-container");
            candidate.matched.forEach(item => {
                let span = document.createElement("span");
                span.className = "badge matched";
                span.textContent = item;
                matchedContainer.appendChild(span);
            });

            if (candidate.matched.length === 0) {
                matchedContainer.innerHTML = "<span style='font-size: 12px; opacity: 0.6;'>None</span>";
            }

            let missingContainer = clone.querySelector(".missing-container");
            candidate.missing.forEach(item => {
                let span = document.createElement("span");
                span.className = "badge missing";
                span.textContent = item;
                missingContainer.appendChild(span);
            });

            if (candidate.missing.length === 0) {
                missingContainer.innerHTML = "<span style='font-size: 12px; opacity: 0.6;'>None</span>";
            }

            if(score >= 65) {
                shortlistedContainer.appendChild(clone);
                hasShortlisted = true;
            } else {
                otherContainer.appendChild(clone);
            }
        });

        if(!hasShortlisted) {
            noShortlisted.style.display = "block";
        }
    })
    .catch(error => {
        console.error("Error analyzing resumes:", error);
        alert("An error occurred analyzing the resumes.");
        submitBtn.disabled = false;
        loading.style.display = "none";
    });
});