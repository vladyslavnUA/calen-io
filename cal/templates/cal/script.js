const btn = document.querySelector('.talk');
const content = document.querySelector('.content');

const greetings = ['hi, how are you doing today']

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.onstart = function() {
    console.log('voice has been ACTIVATED');
};

recognition.onresult = function(event) {
    const current = event.resultIndex;

    const transcript = event.results[current][0].transcript;
    content.textContent = transcript;
    readOutLoud(transcript);
}

btn.addEventListener('click', () => {
    recognition.start();
});


function readOutLoud(message) {
    const speech = new SpeechSynthesisUtterance();
    
    if(message.includes('hello')){
        // const greetMesg = greetings[Math.floor(Math.random() * greetings.length)];
        const greetMesg = 'hi, how are you doing today';
        // const userSaid = voice.onendspeech();
        // console.log(userSaid);
        speech.text = greetMesg;
    }
    if(message.includes('hi')){
        // const greetMesg = greetings[Math.floor(Math.random() * greetings.length)];
        const greetMesg = 'hi, how are you doing today';
        speech.text = greetMesg;
    }

    // if(message.)

    // speech.text = message;
    // speech.onerror = // todo: 'error'
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;

    window.speechSynthesis.speak(speech);
}