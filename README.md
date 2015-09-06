CUET
====

根据cue裁剪专辑

### USAGE

裁剪音频文件需要ffmpeg的支持

有可能需要手动去设定音频的格式（目前默认只写了flac


如果没有ffmpeg，也能获取cue信息 (比如一首歌的时间区间, title等信息
并且可以使用其他音频编码软件

*参考`Cuet.py`*

### REQUIREMENTS

- pyav
    ```
    on MAC

    brew install ffmpeg pkg-config
    pip install av
    ```

