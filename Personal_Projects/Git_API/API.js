import fetch from 'node-fetch';
import prompts from 'prompts';

const questions = [
    {
        type:  'text',
        name: 'repo_owner',
        message: 'Who is the owner of the repo?'
    },

    {
        type: 'text',
        name: 'repo_name',
        message: 'What is the name of the repo?'
    }
];


(async () => {
    try{
        var pagenumber=1;
        var requests =0;
        var pageRequests=1;

        const response = await prompts(questions);

        console.log('Excellent! Querying '+response['repo_owner']+'/'+response['repo_name']+'for open PRs');
        // Create a new request object
        while (pageRequests != 0) {
            const msg = 'https://api.github.com/repos/'+response['repo_owner']+'/'+response['repo_name']+'/pulls?per_page=100&page='+pagenumber;
            await fetch(msg).then(res => {
                    if(!res.ok){
                        throw Error(response.statusText);
                    }
                    else{
                        return res.json();
                    }
                }).then(res => {
                pageRequests = Object.keys(res).length;
                requests += pageRequests;
                pagenumber++;
            })
        }
        console.log('# of open PRs: ' + requests)
        console.log('Bye!')
    }
     catch(e){
        console.log('There was a problem completing the query. It\'s likely that this repo does not exist.')
     }
})();

