# This project is currently under developement


## API documentation

### Token


<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Body</th>
    <th>Response</th>
  </tr>

  <tr>
  <td>/token/</td>
  <td>POST</td>
  <td> 
    <pre lang="typescript">
interface Body {
  username: string;
  password: string;
}</pre>
   </td>
  <td>
    <pre lang="typescript">
interface Response {
  access: string;
  refresh: string;
}</pre>
  </td>
  </tr>

  <tr>
  <td>/token/refresh/</td>
  <td>POST</td>
  <td> 
    <pre lang="typescript">
interface Body {
  refresh: string;
}</pre>
   </td>
  <td>
    <pre lang="typescript">
interface Response {
  access: string;
}</pre>
  </td>
  </tr>
</table>

### User

<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Body</th>
    <th>Response</th>
  </tr>


  <tr>
  <td>/users/</td>
  <td>GET</td>
  <td> - </td>
  <td>
    <pre lang="typescript">
interface Response {
  count: number;
  next: number | null;
  previous: number | null;
  results: {
    id: number;
    username: string;
    display_name: string;
    bio: string;
    website: string;
    location: string;
    birth_date: Date;
    tweets: number[];
    followers: number;
    following: number;
    image_url: string | null;
  }[];
}</pre>
  </td>
</tr>


<tr>
  <td>/users/</td>
  <td>POST</td>
  <td>
    <pre lang="typescript">
interface Body {
  username: string;
  display_name: string;
  password: string;
  image?: File;
}</pre>
  </td>
  <td>
    <pre lang="typescript">
interface Response {
  id: number;
  username: string;
  display_name: string;
  bio: string;
  website: string;
  location: string;
  birth_date: Date;
  tweets: number[];
  followers: number;
  following: number;
  image_url: string | null;
}</pre>
  </td>
</tr>

  <tr>
  <td>/users/&lt;ID&gt;/</td>
  <td>GET</td>
  <td> - </td>
  <td>
    <pre lang="typescript">
interface Response {
  id: number;
  username: string;
  display_name: string;
  bio: string;
  website: string;
  location: string;
  birth_date: Date;
  tweets: number[];
  followers: number;
  following: number;
  image_url: string | null;
}</pre>
  </td>
</tr>


<tr>
  <td>/users/&lt;ID&gt;/</td>
  <td>PUT</td>
  <td>
    <pre lang="typescript">
interface Response {
  username: string;
  display_name: string;
  password: string;
  image: File | null;
}</pre>
  </td>
  <td>
    <pre lang="typescript">
interface Response {
  id: number;
  username: string;
  display_name: string;
  bio: string;
  website: string;
  location: string;
  birth_date: Date;
  tweets: number[];
  followers: number;
  following: number;
  image_url: string | null;
}</pre>
  </td>
</tr>
</table>

### Tweet

<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Body</th>
    <th>Response</th>
  </tr>

<tr>
  <td>/tweets/</td>
  <td>GET</td>
  <td> - </td>
  <td>
    <pre lang="typescript">
interface Response {
  count: number;
  next: number | null;
  previous: number | null;
  results:  {
    id: string;
    text: string | null;
    likes: number;
    comments: number;
    retweets: number;
    retweet: number | null;
    comment: number | null;
    image_url: string | null;
  }[];
}</pre>
  </td>
</tr>

<tr>
  <td>/tweets/</td>
  <td>POST</td>
  <td> 
    <pre lang="typescript">
interface Body {
  text: string;
  comment_id?: number;
  retweet_id?: number;
  image?: File; 
}</pre>
  </td>
  <td>
    <pre lang="typescript">
interface Response {
  id: string;
  text: string;
  likes: number;
  comments: number;
  retweets: number;
  retweet: number | null;
  comment: number | null;
  image_url: string | null;
}</pre>
  </td>
</tr>

<tr>
  <td>/tweets/&lt;ID&gt;/</td>
  <td>GET</td>
  <td> - </td>
  <td>
    <pre lang="typescript">
interface Response {
  id: string;
  text: string;
  likes: number;
  comments: number;
  retweets: number;
  retweet: number | null;
  comment: number | null;
  image_url: string | null;
}</pre>
  </td>
</tr>

<tr>
  <td>/tweets/&lt;ID&gt;/likes/</td>
  <td>GET</td>
  <td> - </td>
  <td>
    <pre lang="typescript">
interface Response {
  count: number;
  next: number | null;
  previous: number | null;
  results:  {
    author: string;
  }[];
}</pre>
  </td>
</tr>

<tr>
  <td>/tweets/&lt;ID&gt;/retweet/</td>
  <td>GET</td>
  <td> - </td>
  <td>
    <pre lang="typescript">
interface Response {
  id: string;
  text: string;
  likes: number;
  comments: number;
  retweets: number;
  retweet: number | null;
  comment: number | null;
  image_url: string | null;
}</pre>
  </td>
</tr>

 <tr>
  <td>/tweets/&lt;ID&gt;/retweets/</td>
  <td>GET</td>
  <td> - </td>
  <td>
    <pre lang="typescript">
interface Response {
  count: number;
  next: number | null;
  previous: number | null;
  results:  {
    id: string;
    text: string | null;
    likes: number;
    comments: number;
    retweets: number;
    retweet: number | null;
    comment: number | null;
    image_url: string | null;
  }[];
}</pre>
  </td>
</tr>

<tr>
  <td>/tweets/&lt;ID&gt;/comment/</td>
  <td>GET</td>
  <td> - </td>
  <td>
    <pre lang="typescript">
interface Response {
  id: string;
  text: string;
  likes: number;
  comments: number;
  retweets: number;
  retweet: number | null;
  comment: number | null;
  image_url: string | null;
}</pre>
  </td>
</tr>

 <tr>
  <td>/tweets/&lt;ID&gt;/comments/</td>
  <td>GET</td>
  <td> - </td>
  <td>
    <pre lang="typescript">
interface Response {
  count: number;
  next: number | null;
  previous: number | null;
  results:  {
    id: string;
    text: string | null;
    likes: number;
    comments: number;
    retweets: number;
    retweet: number | null;
    comment: number | null;
    image_url: string | null;
  }[];
}</pre>
  </td>
</tr>

<tr>
  <td>/tweets/&lt;ID&gt;/</td>
  <td>DELETE</td>
  <td> - </td>
  <td> - </td>
</tr>

</table>


### Like


<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Body</th>
    <th>Response</th>
  </tr>

<tr>
  <td>/likes/</td>
  <td>POST</td>
  <td> 
    <pre lang="typescript">
interface Body {
  tweet_id: string;
}</pre>
  </td>
  <td>
    <pre lang="typescript">
interface Response {
  author: string;
}</pre>
  </td>

<tr>
  <td>/likes/&lt;TWEET_ID&gt;/</td>
  <td>DELETE</td>
  <td> - </td>
  <td> - </td>
</tr>

</tr>

</table>


### Follow


<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Body</th>
    <th>Response</th>
  </tr>


<tr>
  <td>/follow/</td>
  <td>POST</td>
  <td> 
    <pre lang="typescript">
interface Body {
  being_followed: number;
}</pre>
  </td>
  <td>
    <pre lang="typescript">
interface Response {
  following: number;
  being_followed: number;
}</pre>
  </td>

<tr>
  <td>/follow/&lt;PROFILE_ID&gt;/</td>
  <td>DELETE</td>
  <td> - </td>
  <td> - </td>
</tr>

</tr>


</table>
