import { userHeaderComponent, noticeComponent, postComponent } from "./components.js";

/// Vue.js apps
const ticktockApp = Vue.createApp({
    components: {
        "userheader": userHeaderComponent,
        "post": postComponent,
        "notice": noticeComponent,
    },
    data() {
        return {
            posts: [],
            selected_users: [],
        };
    },
    delimiters: [ "[[", "]]" ],
    methods: {
        _get_posts_from_endpoint(endpoint) {
            fetch(endpoint)
                .then(data => { return data.json() })
                .then(data => {
                    this.$data.posts = data.posts;
                })
                .catch(error => {
                    console.log("Error fetching posts: " + error);
                });
        },
        set_selected_user(uid) {
            fetch("/api/user/" + uid)
                .then(data => { return data.json() })
                .then(data => {
                    this.$data.selected_users = [data];
                })
                .catch(error => {
                    console.log("Error: unable to fetch user info from /api/user/" + uid);
                });
        },
        get_recent_posts() {
            return this._get_posts_from_endpoint("/api/posts/recent");
        },
        get_user_posts(uid) {
            return this._get_posts_from_endpoint("/api/posts/user/" + uid);
        },
        get_post(post_id) {
            fetch("/api/posts/id/" + post_id)
                .then(data => { return data.json() })
                .then(data => {
                    this.$data.posts = [data];
                })
                .catch(error => {
                    console.log("Error fetching posts: " + error);
                });
        },
    },
});

const ticktockAppVm = ticktockApp.mount("#ticktockApp");

// Update the clock periodically
window.setInterval(() => {
    let current_time = new Date();
    let el = document.getElementById("navClock");
    el.innerText = current_time.toLocaleTimeString();
}, 500);

export {
    ticktockAppVm,
};
