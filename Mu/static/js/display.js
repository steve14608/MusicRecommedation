const audio = document.getElementById('audio');
const lyricsContainer = document.getElementById('lyrics');
const progressBar = document.querySelector('.progress');
const songCurrentTime=document.querySelector('.current-time');
const songEndTime=document.querySelector('.duration');
const displayButton=document.querySelector('.play-pause');
const prevButton=document.querySelector('.prev');
const nextButton=document.querySelector('.next');

//前端处理后端传入的歌词并读取显示出来
const inputStr = `{'lyric': '[ 
        00: 00.00 
    ] 作词 : 小寒\n[ 
        00: 01.00 
    ] 作曲 : 方大同\n[ 
        00: 02.00 
    ] 编曲 : 方大同/Edward Chan\n[ 
        00: 17.03 
    ]欢笑声 欢呼声\n[ 
        00: 20.52 
    ]炒热气氛 心却很冷\n[ 
        00: 24.29 
    ]聚光灯 是种蒙恩\n[ 
        00: 27.95 
    ]我却不能 喊等一等\n[ 
        00: 31.42 
    ]我真佩服我 还能幽默\n[ 
        00: 35.03 
    ]掉眼泪时 用笑掩过\n[ 
        00: 38.78 
    ]怕人看破 顾虑好多\n[ 
        00: 42.50 
    ]不谈寂寞 我们就都快活\n[ 
        00: 48.40 
    ]我不唱声嘶力竭的情歌\n[ 
        00: 55.62 
    ]不表示没有心碎的时刻\n[ 
        01: 02.63 
    ]我不曾摊开伤口任宰割\n[ 
        01: 08.53 
    ]愈合 就无人晓得\n[ 
        01: 13.43 
    ]我内心挫折\n[ 
        01: 16.99 
    ]活像个孤独患者 自我拉扯\n[ 
        01: 24.27 
    ]外向的孤独患者 有何不可\n[ 
        01: 39.90 
    ]笑越大声 越是残忍\n[ 
        01: 43.45 
    ]挤满体温 室温更冷\n[ 
        01: 47.02 
    ]万一关灯 空虚扰人\n[ 
        01: 50.62 
    ]我却不能 喊等一等\n[ 
        01: 54.12 
    ]你说你爱我 却一直说\n[ 
        01: 57.57 
    ]说我不该 窝在角落\n[ 
        02: 01.18 
    ]策划逃脱 这也有错\n[ 
        02: 04.91 
    ]连我脆弱 的权利都掠夺\n[ 
        02: 10.85 
    ]我不唱声嘶力竭的情歌\n[ 
        02: 17.83 
    ]不表示没有心碎的时刻\n[ 
        02: 24.80 
    ]我不曾摊开伤口任宰割\n[ 
        02: 30.79 
    ]愈合 就无人晓得\n[ 
        02: 35.49 
    ]我内心挫折\n[ 
        02: 39.05 
    ]活像个孤独患者 自我拉扯\n[ 
        02: 46.07 
    ]外向的孤独患者 有何不可\n[ 
        03: 21.52 
    ]我不要声嘶力竭的情歌\n[ 
        03: 28.75 
    ]来提示我需要你的时刻\n[ 
        03: 35.59 
    ]表面镇定并不是保护色\n[ 
        03: 41.47 
    ]反而 是要你懂得\n[ 
        03: 46.10 
    ]我不知为何\n[ 
        03: 49.87 
    ]活像个孤独患者 自我拉扯\n[ 
        03: 57.01 
    ]外向的孤独患者 需要认可\n[ 
        04: 30.09 
    ]监制 : Edward Chan / Charles Lee / 方大同\n'}`;

const pattern = /\[\s*(\d{2}):\s*(\d{2})\.(\d{2})\s*\](.*?)\n/g;

const resultStr = inputStr.replace(pattern, (match, minutes, seconds, milliseconds, lyric) => {
    const timeInSeconds = parseInt(minutes) * 60 + parseInt(seconds) + parseInt(milliseconds) / 100;
    return `[ ${timeInSeconds.toFixed(2)} ]${lyric.trim()}\n`;
});

const cleanedStr = resultStr.replace("{'lyric': '", '').trim();
const lines = cleanedStr.split('\n').filter(line => line.trim() !== '');
const lyricsData = lines.map(line => {
    const timePattern = /\[\s*(\d+(\.\d+)?)\s*\]/; 
    const timeMatch = line.match(timePattern);
    const time = timeMatch ? timeMatch[1] : null; 

    const lyric = line.replace(timePattern, '').trim(); 
    return [time, lyric]; 
});

let currentLyricIndex = -1;

function updateLyrics() {
  const currentTime = audio.currentTime; 
  for (let i = 0; i < lyricsData.length; i++) {
    if (currentTime >= lyricsData[i][0] && (i === lyricsData.length - 1 || currentTime < lyricsData[i + 1][0])) {
      if (i !== currentLyricIndex) {
        currentLyricIndex = i;
        renderLyrics(i);
      }
      break;
    }
  }
}

function renderLyrics(index) {
  lyricsContainer.innerHTML = "";

  const lyricElement = document.createElement('lyrics');
  songCurrentTime.textContent=audio.currentTime;
  lyricElement.textContent = lyricsData[index][1];
  lyricElement.classList.add('current-lyric'); 
  lyricsContainer.appendChild(lyricElement);
}

audio.addEventListener('timeupdate', updateLyrics);

renderLyrics(0);
    


//处理progressBar
audio.addEventListener('timeupdate', ()=>{
    songCurrentTime.textContent=formatTime(audio.currentTime);
    progressBar.value = audio.currentTime;
});
audio.addEventListener('loadedmetadata', () => {
    songEndTime.textContent = formatTime(audio.duration);
    progressBar.max = audio.duration; 
});
audio.addEventListener('ended', () => {
    displayButton.textContent='⏯';
});
progressBar.addEventListener('input', (event) => {
    audio.currentTime = event.target.value;
});
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}
displayButton.addEventListener('click', function () {
    let button = this;
    if (button.textContent === '⏯') {
        audio.play();
        button.textContent = '⏸'; 
    } else {
        audio.pause();
        button.textContent = '⏯'; 
    }
});

prevButton.addEventListener('click', function () {
    alert('上一首歌');
});

nextButton.addEventListener('click', function () {
    alert('下一首歌');
});

