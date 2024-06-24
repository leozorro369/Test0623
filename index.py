<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Online Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .question {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Online Test</h1>
    <form id="testForm">
        <!-- Questions will be dynamically inserted here -->
    </form>
    <button type="button" onclick="submitTest()">Submit</button>
    <div id="result"></div>
    
    <script>
        fetch('questions.json')
            .then(response => response.json())
            .then(data => loadQuestions(data));

        function loadQuestions(questions) {
            const form = document.getElementById('testForm');

            // Load fill in the blank questions
            questions.fill_in_the_blank.forEach((q, index) => {
                const div = document.createElement('div');
                div.className = 'question';
                div.innerHTML = `<label>${index + 1}. ${q}</label><br><input type="text" name="fill_in_the_blank_${index}"><br>`;
                form.appendChild(div);
            });

            // Load single choice questions
            questions.single_choice.forEach((q, index) => {
                const div = document.createElement('div');
                div.className = 'question';
                div.innerHTML = `<label>${index + 1}. ${q}</label><br>`;
                q.options.forEach(option => {
                    div.innerHTML += `<input type="radio" name="single_choice_${index}" value="${option}"> ${option}<br>`;
                });
                form.appendChild(div);
            });

            // Load multiple choice questions
            questions.multiple_choice.forEach((q, index) => {
                const div = document.createElement('div');
                div.className = 'question';
                div.innerHTML = `<label>${index + 1}. ${q}</label><br>`;
                q.options.forEach(option => {
                    div.innerHTML += `<input type="checkbox" name="multiple_choice_${index}" value="${option}"> ${option}<br>`;
                });
                form.appendChild(div);
            });

            // Load true/false questions
            questions.true_false.forEach((q, index) => {
                const div = document.createElement('div');
                div.className = 'question';
                div.innerHTML = `<label>${index + 1}. ${q}</label><br>
                                 <input type="radio" name="true_false_${index}" value="对"> 对<br>
                                 <input type="radio" name="true_false_${index}" value="错"> 错<br>`;
                form.appendChild(div);
            });

            // Load case analysis questions
            questions.case_analysis.forEach((q, index) => {
                const div = document.createElement('div');
                div.className = 'question';
                div.innerHTML = `<label>${index + 1}. ${q}</label><br><textarea name="case_analysis_${index}" rows="4" cols="50"></textarea><br>`;
                form.appendChild(div);
            });
        }

        function submitTest() {
            const form = document.getElementById('testForm');
            const formData = new FormData(form);
            const answers = {};
            formData.forEach((value, key) => {
                if (answers[key]) {
                    if (!Array.isArray(answers[key])) {
                        answers[key] = [answers[key]];
                    }
                    answers[key].push(value);
                } else {
                    answers[key] = value;
                }
            });

            fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(answers)
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerHTML = `Your score: ${data.score}`;
            });
        }
    </script>
</body>
</html>
