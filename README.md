Configuration file syntax
=========================

Configuration is done with a json file:

```
{
    "01 my scenario": {
        "01 my first scene": [
            {
                "path": "/home/me/sounds/great_music.wav",
                "loop": true
            },
            {
                "path": "/home/me/sounds/wolves.wav",
                "loop": false,
                "start_at": 10,
                "volume": 70,
                "random": 0.2
            }
        ],
        "02 my second scene": [
            {
                "path": "/home/me/sounds/thunder.wav",
                "loop": true
            }
        ]
    }
}
```
