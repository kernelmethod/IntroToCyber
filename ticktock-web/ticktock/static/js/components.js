/* Vue.js components for TickTock */

const userHeaderComponent = {
    props: ["username", "uid"],
    template: `\
<h3 class="container">
    <a v-bind:href="'/user/' + username">
    <div class="user-header">
    <img v-if="uid" class="profile-img" v-bind:src="'/s3/avatar/' + uid">
    <span v-if="username" class="username">{{ username }}</span>
    </div>
    </a>
</h3>
`,
    data() {
      return {
        visible: false,
      }
    },
}

const postComponent = {
    props: ["username", "post_id", "content", "posted", "uid"],
    template: `\
<div class="post">
<a v-bind:href="'/post?id=' + post_id">
    <div class="inner">
    <userheader v-bind:username="username" v-bind:uid="uid">
    </userheader>
    <p v-html="content"></p>
    <p class="text-light">Posted at {{ this.convertDateString() }}</p>
    </div>
</a>
</div>
`,
    methods: {
        convertDateString() {
            let timestamp = Date.parse(this.posted);
            return new Date(timestamp).toLocaleString();
        }
    },
    components: {
        "userheader": userHeaderComponent,
    },
};

const noticeComponent = {
    props: ["level", "header"],
    template: `\
<div class="notice">
  <div v-bind:class="this.levelAttrs().cssclass">
    <b>{{ this.levelAttrs().default_header }}: </b>
    <slot></slot>
  </div>
</div>
`,
    methods: {
        levelAttrs() {
            switch (this.level) {
                case "info":
                    return { cssclass: "notice-info", default_header: "Info" };
                case "warning":
                    return { cssclass: "notice-warning", default_header: "Warning" };
                case "error":
                    return { cssclass: "notice-error", default_header: "Error" };
                default:
                    return { cssclass: "notice-unknown", default_header: "Unknown" };
            }
        },
    },
};

export {
    userHeaderComponent,
    noticeComponent,
    postComponent,
};
