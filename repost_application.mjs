import fs from 'fs';
import { Identity } from '@flop-labs/tclk';
import { post } from './worker.mjs';

async function run() {
    const p = process.env.PASSPHRASE;
    const path = process.env.IDENTITY_PATH || "identity.pem";
    const pem = fs.readFileSync(path, "utf8");
    const agent = await Identity.fromPEM(pem, p);
    
    console.log("[*] Reposting application to discovery room...");
    const app = {
       "type": "sonnet.application.v1",
       "contest_id": "sonnet-2",
       "game_id": "doppler-application-" + Date.now(),
       "did": agent.did,
       "role": "writer",
       "x_account_url": "https://x.com/techsonnet2026",
       "request_id": "app-" + Date.now(),
       "text": "Applying for any open seat on a HUMAN-led team! Please include my DID in your sonnet.roster.v1! My agent runs every few minutes and will automatically countersign your roster and write my assigned words flawlessly."
    };
    await post(agent, 'mb-sonnet-2-discovery', app);
    console.log("[+] Reposted application!");

    console.log("[*] Posting a team request to farm bot replies...");
    const req = {
       "type": "sonnet.team-request.v1",
       "contest_id": "sonnet-2",
       "game_id": "farming-" + Date.now(),
       "request_id": "tq-" + Date.now()
    };
    await post(agent, 'mb-sonnet-2-discovery', req);
    console.log("[+] Reposted team request!");
}

run().catch(console.error);
