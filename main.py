
from dataclasses import dataclass
from drafter import *

set_website_title("Music Mood Matcher")
set_site_information(
    author="Ayden Bleiler",
    description="To help you find music based on your mood.",
    sources="Thanks to the Drafter docs and my study group.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/ableiler/Music_mood_matcher"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Song:
    title: str
    artist: str
    genre: str
    mood: str
    link: str

@dataclass
class State:
    mood: str
    genre: str
    num_songs: str
    songs: list[Song]
    favorites: list[Song]
    selected_song_title: str

@route
def index(state: State) -> Page:
    """Displays the homepage and welcomes users to the Music Mood Matcher."""
    return Page(state, [
        Header("Welcome to the Music Mood Matcher! 🎶"),
        "Find the perfect songs based on your current mood and favorite genre.",
        Button("Get Started", "select_mood")
    ])

@route
def select_mood(state: State) -> Page:
    """Allows users to select their current mood."""
    return Page(state, [
        Header("Select Your Mood"),
        "Choose your current mood:",
        SelectBox("mood", ["Happy", "Sad", "Relaxed", "Energetic"]),
        Button("Next: Choose Genre", "select_genre")
    ])

@route
def select_genre(state: State, mood: str) -> Page:
    """Allows users to choose their preferred music genre and how many songs they want."""
    state.mood = mood
    return Page(state, [
        Header("Select Your Genre & Quantity"),
        "Choose your favorite genre:",
        SelectBox("genre", ["Pop", "Rap", "R&B", "Rock"]),
        "How many songs do you want? (Enter 1, 2, 3, 4, or 5)",
        TextBox("num_songs", "3"),
        Button("Get Recommendations", "get_recommendations")
    ])

@route
def get_recommendations(state: State, genre: str, num_songs: str) -> Page:
    """Filters the song list based on the user's selected mood and genre."""
    
    state.genre = genre
    state.num_songs = num_songs
    
    # Determine the limit using pure string comparisons without converting to int
    limit = 3
    if state.num_songs == "1":
        limit = 1
    elif state.num_songs == "2":
        limit = 2
    elif state.num_songs == "3":
        limit = 3
    elif state.num_songs == "4":
        limit = 4
    elif state.num_songs == "5":
        limit = 5

    matched_songs = []
    
    # Loop to iterate over the list of dataclass instances and filter
    for song in state.songs:
        if song.mood.lower() == state.mood.lower() and song.genre.lower() == state.genre.lower():
            if len(matched_songs) < limit:
                matched_songs.append(song)
    
    components = [Header("Your Song Recommendations")]
    
    if not matched_songs:
        components.append("No songs matched your exact criteria. Try going back and choosing different options!")
    else:
        for song in matched_songs:
            components.append(song.title + " by " + song.artist)
            components.append("Genre: " + song.genre + " | Mood: " + song.mood)
            components.append(Link("Listen Here", song.link))
            components.append(Button(
                "Add to Favorites",
                "add_favorite",
                [("selected_song_title", song.title)]
            ))
            
    components.append(Button("View Favorites", "view_favorites"))
    components.append(Button("Start Over", "index"))
    
    return Page(state, components)

@route
def add_favorite(state: State, selected_song_title: str) -> Page:
    """Adds a selected song to the user's favorites list."""
    state.selected_song_title = selected_song_title
    for song in state.songs:
        if song.title == state.selected_song_title:
            if song not in state.favorites:
                state.favorites.append(song)
    return view_favorites(state)

@route
def view_favorites(state: State) -> Page:
    """Displays all songs the user has saved as favorites."""
    components = [Header("Your Favorite Songs")]
    
    if not state.favorites:
        components.append("You haven't saved any favorites yet.")
    else:
        for song in state.favorites:
            components.append(song.title + " by " + song.artist)
            components.append(Button(
                "Remove",
                "remove_favorite",
                [("selected_song_title", song.title)]
            ))
    
    components.append(Button("Return Home", "index"))
    return Page(state, components)

@route
def remove_favorite(state: State, selected_song_title: str) -> Page:
    """Removes a selected song from the favorites list."""
    state.selected_song_title = selected_song_title
    state.favorites = [song for song in state.favorites if song.title != state.selected_song_title]
    return view_favorites(state)

# Initial global data objects
initial_songs = [
    Song("Happy Song", "Artist A", "Pop", "Happy", "https://example.com/song1"),
    Song("Chill Beats", "Artist B", "R&B", "Relaxed", "https://example.com/song2"),
    Song("Energy Boost", "Artist C", "Rock", "Energetic", "https://example.com/song3"),
    Song("Rainy Days", "Artist D", "Pop", "Sad", "https://example.com/song4"),
    Song("Party Anthem", "Artist E", "Rap", "Energetic", "https://example.com/song5")
]

start_server(
    State(
        "Happy",
        "Pop",
        "3",
        initial_songs,
        [],
        ""
    )
)

