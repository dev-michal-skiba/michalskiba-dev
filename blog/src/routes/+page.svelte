<script>
	/** @type {import('./$types').PageData} */
	export let data;
</script>

{#each data.posts as post}
    <a class="div-link" href="/post/{post.slug}">
        <div class="container-md blog-post-tile">
            <h2>{post.title}</h2>
            <p>{@html post.lead}</p>
        </div>
    </a>
{/each}
