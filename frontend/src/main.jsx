import React from 'react';
import {createRoot} from 'react-dom/client';

function App(){
return <div>
<h1>⚽ FootballVerse</h1>
<h2>Football Story Studio</h2>
<p>Documentaries • Legends • History • Creator Studio</p>
<button>New Story</button>
<button>Upload Media</button>
<h3>Modules</h3>
<ul>
<li>Stories</li>
<li>Players</li>
<li>Clubs</li>
<li>Media Library</li>
<li>Video Editor Ready</li>
<li>Admin Panel Ready</li>
</ul>
</div>
}
createRoot(document.getElementById('root')).render(<App/>)
