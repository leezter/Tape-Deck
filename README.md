# 🎵 Tape Deck - Your Personal Movie Collection Manager 🎥

Welcome to **Tape Deck**, the coolest way to manage your personal movie collection! Whether you're a movie buff or just someone who loves keeping track of their favorite films, Tape Deck has got you covered. With a sleek interface and powerful features, you'll never lose track of your favorite movies again.

## Features

- **User Management**: Add and manage users effortlessly.
- **Movie Collection**: Add, update, and delete movies for each user.
- **OMDb API Integration**: Automatically fetch movie details like director, year, rating, and even the cover image.
- **Responsive Design**: Enjoy a modern, responsive UI that looks great on any device.
- **Custom Error Pages**: Get a friendly 404 page when something goes wrong.
- **Grid Layout**: Movies are displayed in a beautiful grid format for easy browsing.

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS (with a dark theme and red accents for that cinematic feel!)
- **API**: OMDb API for fetching movie details

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/tape-deck.git
   cd tape-deck
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the `.env` file:
   ```
   OMDB_API_KEY=your_omdb_api_key_here
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000`.

## Folder Structure

```
Tape-Deck/
├── app.py               # Main application file
├── datamanager/         # Contains database models and data management logic
├── templates/           # HTML templates for the app
├── static/              # Static files (CSS, images, etc.)
├── data/                # SQLite database file
├── instance/            # Instance folder for database
├── .env                 # Environment variables (not included in version control)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Contributing

Feel free to fork this repository and submit pull requests. Let's make Tape Deck even better together!

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Enjoy managing your movie collection with Tape Deck! 🎬
