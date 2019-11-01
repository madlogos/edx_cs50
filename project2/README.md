# Project 2

Web Programming with Python and JavaScript

It meets the project requirements:

- [x] Display Name: When a user visits your web application for the first time, they should be prompted to type in a display name that will eventually be associated with every message the user sends. If a user closes the page and returns to your app later, the display name should still be remembered.
    - The first time a user enters the system, a pop-up will show to ask him/her to enter a display name. The user info will be stored in `session` data.
- [x] Channel Creation: Any user should be able to create a new channel, so long as its name doesn’t conflict with the name of an existing channel.
    - After the user is created, he/she can create a channel. If the name conflicts with existing channels, a `flash` alert will show.
- [x] Channel List: Users should be able to see a list of all current channels, and selecting one should allow the user to view the channel. We leave it to you to decide how to display such a list.
    - A global dict object `channels` is created to store channels as well as the last 100 posts. User can see the channel list on `/channels` page. The last channel he/she visited is stored in the global dict object `users`, and thus show on the page for a quick visit.
- [x] Messages View: Once a channel is selected, the user should see any messages that have already been sent in that channel, up to a maximum of 100 messages. Your app should only store the 100 most recent messages per channel in server-side memory.
    - When the user enters a specific channel, he/she can see the last 100 existing posts on the `channel/<channel>` page.
- [x] Sending Messages: Once in a channel, users should be able to send text messages to others the channel. When a user sends a message, their display name and the timestamp of the message should be associated with the message. All users in the channel should then see the new message (with display name and timestamp) appear on their channel page. Sending and receiving messages should NOT require reloading the page.
    - User can submit his/her message by clicking <kbd>Send</kbd> on the page, or pressing <kbd>Shift+Enter</kbd>. The messages will show in the table.
- [x] Remembering the Channel: If a user is on a channel page, closes the web browser window, and goes back to your web application, your application should remember what channel the user was on previously and take the user back to that channel.
    - The latest visited channel is stored in the `users` global object.
- [x] Personal Touch: Add at least one additional feature to your chat application of your choosing! Feel free to be creative, but if you’re looking for ideas, possibilities include: supporting deleting one’s own messages, supporting use attachments (file uploads) as messages, or supporting private messaging between two users.
    - The user can delete his/her posts, but cannot delete others'.