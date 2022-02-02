import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';


function App() {
  const args = JSON.parse(document.getElementById("data").text);
  const [artist_list_before, setBeforeList] = useState([]);
  const [artist_list_after, setAfterList] = useState(args.artist_id_list);
  const user_input = useRef(null);

  function add_artist() {
    if (user_input.current.value != "") {
      let new_artist = user_input.current.value;
      let new_artist_List = [...artist_list_before, new_artist];
      setBeforeList(new_artist_List);
      user_input.current.value = "";
    }
  }

  function delete_artist(i) {
    let list = [...artist_list_after.slice(0, i), ...artist_list_after.slice(i + 1)];
    setAfterList(list);
    /*
            fetch('/delete_artist', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ "artist_list": artist_list_after }),
            }).then(response => response.json()).then(data => {
              setAfterList(data.after_delete);
            });
    
    
            <ul>
                {artist_list_after.map((artist_name, index) => (
                  <>
                    <li key={index}> {artist_name} </li><br />
                  </>
                ))}
              </ul>
    */
  }

  function deleteartist(id) {
    fetch('/delete_artist', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "id": id }),
    }).then(response => response.json()).then(data => {
      setAfterList(data.after_delete);
      window.location.reload();
    });
  }

  const artistList = artist_list_after.map((artist, i) => (
    <div>
      <p>{artist}</p>
      <button onClick={() => deleteartist(artist)}>delete</button>
    </div>
  ));

  function save_to_db() {
    fetch('/add_artist_to_db', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "artist_name": artist_list_before }),
    }).then(response => response.json()).then(data => {
      if (data.input_server == false) {
        alert("Invalid artist included! Please try again");
        let reset_list = artist_list_before.filter(artist_list_before => artist_list_before !== artist_list_before);
        setBeforeList(reset_list);
      } else {
        let new_artist = data.input_server;
        let new_list = [...artist_list_after, new_artist];
        setAfterList(new_list);
        let reset_list = artist_list_before.filter(artist_list_before => artist_list_before !== artist_list_before);
        setBeforeList(reset_list);
      }
    });
  }

  return (
    <>
      <div class='grid_container'>
        <div class='one'>
          <h2> Search artist by name: </h2>
          <form method="POST" action="/main">
            <input ref={user_input} type="text" name="artist_name" placeholder="Artist name" />
            <input type="submit" value="Reload" />
          </form>
          <br />
          <button onClick={add_artist}>Add to list</button>
          <button onClick={save_to_db}>Save list to DB </button>
          <h2> Artist List so far </h2>
          <ul>
            {artist_list_before.map((artist, index) => (
              <><li key={index}> {artist} </li><br /></>
            ))}
          </ul>
        </div>

        <div class='two'>
          <div class='song_name'> {args.song_name} </div>
          <div class='artist_name'> {args.artist_name} </div>
          <div> <img src={args.song_image} alt="Album Cover" width={640} height={640} /> </div>
        </div>

        <div class='three'>
          <h1> Artist List in DB </h1>
          {artistList}
        </div>

        <div class='four'><a href={args.lyrics_url}>somewhat related lyrics here</a></div>
        <div class='five'><audio controls src={args.song_preview}></audio></div>
      </div>
    </>
  );
}

export default App;
