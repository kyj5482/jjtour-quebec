"""Render the role-play / badge phrases to natural Quebec French (and U.S. English) MP3s with edge-tts.
usage: node -e (see README) > utter.json; python3 src/make_audio.py utter.json audio src/audio_index.json"""
import json, sys, asyncio, hashlib, os
import edge_tts
U=json.load(open(sys.argv[1])); OUT=sys.argv[2]; os.makedirs(OUT, exist_ok=True)
VOICE={("fr","T"):"fr-CA-SylvieNeural",("fr","M"):"fr-CA-AntoineNeural",("en","T"):"en-US-JennyNeural",("en","M"):"en-US-AndrewNeural"}
idx={}
async def one(u, sem):
    v=VOICE[(u["lang"],u["role"])]; key=f'{u["lang"]}|{u["role"]}|{u["text"]}'
    h=hashlib.sha1(f"{v}|{u['text']}".encode()).hexdigest()[:12]; idx[key]=h
    async with sem:
        for rate,suf in [("+0%",""),("-25%","_s")]:
            f=f"{OUT}/{h}{suf}.mp3"
            if os.path.exists(f) and os.path.getsize(f)>500: continue
            for a in range(4):
                try:
                    await edge_tts.Communicate(u["text"], v, rate=rate).save(f); break
                except Exception as e:
                    print("retry",h,e); await asyncio.sleep(2+a*3)
async def main():
    sem=asyncio.Semaphore(4)
    await asyncio.gather(*[one(u,sem) for u in U])
    json.dump(idx, open(sys.argv[3],"w"), ensure_ascii=False, indent=0)
asyncio.run(main())
print(len(idx), "clips")
