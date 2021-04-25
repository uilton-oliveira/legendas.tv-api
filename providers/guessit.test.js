const guessit = require('./guessit');

test('guess should work as expected', () => {
    return guessit.guess('Grimm.S01E21.720p.HDTV.X264-DIMENSION.mkv')
        .then(response => {
            const data = response.data;
            expect(data.title).toEqual("Grimm");
            expect(data.type).toEqual('episode');
            expect(data.season).toEqual(1);
            expect(data.episode).toEqual(21);
            expect(data.mimetype).toEqual('video/x-matroska');
            expect(data.screen_size).toEqual('720p');
            expect(data.source).toEqual('HDTV');
            expect(data.release_group).toEqual('DIMENSION');
            expect(data.video_codec).toEqual('H.264');
            expect(data.container).toEqual('mkv');
        });
});

test('guess should work as expected, more complex case', () => {
    return guessit.guess('The.100.S05E13.Damocles.Part.2.720p.NF.WEB-DL.DD5.1.x264-CasStudio.mp4')
        .then(response => {
            const data = response.data;
            expect(data.title).toEqual("The 100");
            expect(data.type).toEqual('episode');
            expect(data.season).toEqual(5);
            expect(data.episode).toEqual(13);
            expect(data.mimetype).toEqual('video/mp4');
            expect(data.screen_size).toEqual('720p');
            expect(data.source).toEqual('Web');
            expect(data.release_group).toEqual('CasStudio');
            expect(data.video_codec).toEqual('H.264');
            expect(data.container).toEqual('mp4');
            expect(data.streaming_service).toEqual('Netflix');
            expect(data.episode_title).toEqual('Damocles');
            expect(data.audio_channels).toEqual('5.1');
            expect(data.audio_codec).toEqual('Dolby Digital');
            expect(data.part).toEqual(2);
        });
});

test('batch should work', () => {
    return guessit.batch([
        'Grimm.S01E21.720p.HDTV.X264-DIMENSION.mkv',
        'The.100.S05E13.Damocles.Part.2.720p.NF.WEB-DL.DD5.1.x264-CasStudio.mp4'
    ]).then(response => {
        const data = response.data;
        const data0 = data[0];
        expect(data0.title).toEqual("Grimm");
        expect(data0.type).toEqual('episode');
        expect(data0.season).toEqual(1);
        expect(data0.episode).toEqual(21);
        expect(data0.mimetype).toEqual('video/x-matroska');
        expect(data0.screen_size).toEqual('720p');
        expect(data0.source).toEqual('HDTV');
        expect(data0.release_group).toEqual('DIMENSION');
        expect(data0.video_codec).toEqual('H.264');
        expect(data0.container).toEqual('mkv');

        const data1 = data[1];
        expect(data1.title).toEqual("The 100");
        expect(data1.type).toEqual('episode');
        expect(data1.season).toEqual(5);
        expect(data1.episode).toEqual(13);
        expect(data1.mimetype).toEqual('video/mp4');
        expect(data1.screen_size).toEqual('720p');
        expect(data1.source).toEqual('Web');
        expect(data1.release_group).toEqual('CasStudio');
        expect(data1.video_codec).toEqual('H.264');
        expect(data1.container).toEqual('mp4');
        expect(data1.streaming_service).toEqual('Netflix');
        expect(data1.episode_title).toEqual('Damocles');
        expect(data1.audio_channels).toEqual('5.1');
        expect(data1.audio_codec).toEqual('Dolby Digital');
        expect(data1.part).toEqual(2);
    });
});

test('chooseBest should work as expected', () => {
    return guessit.chooseBest([
        'The.100.S05E13.WEB.x264-TBS-ION10-CasStudio-METCON',
        'The.100.S05E12.WEB.x264-TBS-ION10-CasStudio-METCON',
        'The.100.S04E13.WEB.x264-TBS-ION10-CasStudio-METCON',
        'The.100.S05E13.720p.HDTV.x264-KILLERS',
        'The.100.S05E13.1080p.HDTV.x264-KILLERS',
        'The.100.S05E13.1080p.HDTV.x264-METCON',
        'The.100.S05E13.720p.WEB-DL.x264-METCON'
    ], 
    'The.100.S05E13.Damocles.Part.2.720p.NF.WEB-DL.DD5.1.x264-CasStudio.mp4')
    .then(data => {
        expect(data).toEqual('The.100.S05E13.WEB.x264-TBS-ION10-CasStudio-METCON')
    });
});

test('chooseBest should work as expected, with streaming_service', () => {
    return guessit.chooseBest([
        'The.100.S05E13.WEB.x264-TBS-ION10-CasStudio-METCON',
        'The.100.S05E13.WEB.NF.x264-TBS-ION10-CasStudio-METCON',
        'The.100.S05E12.WEB.x264-TBS-ION10-CasStudio-METCON',
        'The.100.S04E13.WEB.x264-TBS-ION10-CasStudio-METCON',
        'The.100.S05E13.720p.HDTV.x264-KILLERS',
        'The.100.S05E13.1080p.HDTV.x264-KILLERS',
        'The.100.S05E13.1080p.HDTV.x264-METCON',
        'The.100.S05E13.720p.WEB-DL.x264-METCON'
    ], 
    'The.100.S05E13.Damocles.Part.2.720p.NF.WEB-DL.DD5.1.x264-CasStudio.mp4')
    .then(data => {
        expect(data).toEqual('The.100.S05E13.WEB.NF.x264-TBS-ION10-CasStudio-METCON')
    });
});