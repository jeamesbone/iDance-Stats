iDance-Stats
============

This project is a web application designed to view and maintain statistics exported from the iDance game/exercise platform.

The app takes the raw xml data exported from iDance and imports it into the internal (currently sqlite for convenience) database.

Currently implemented features:

  * Importing of new data from the iDance xml export
  * Viewing/Sorting/Filtering of System wide high scores
  * Viewing/Sorting/Filtering of scores per player
  * Viewing/Sorting/Filtering of scores per song
  * A "Match-Up" feature, where 2 players can find songs where they have similar scores (regardless of difficulty)
    * This feature is intended be used for the "Head-to-head" format at Stomp Fitness

Features to be implemented

  * Achievement System
  * User Profiles
    * Graphs/Analytics (Average score over time, session statistics etc.)
    * Achievements earned
    * Best scores, high scores
  * Compare feature to compare scores etc. to other players
