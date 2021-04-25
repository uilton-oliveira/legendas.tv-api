const legendastv = require('./legendastv');

test('no result found should return empty releases and last page', () => {
    return legendastv.search('Something that should be invalid')
        .then(data => {
            expect(data).toHaveProperty("last_page", true);
            expect(data).toHaveProperty("releases", []);
        });
});

test('results found should return non empty releases and have the search term in elements', () => {
    const searchTerm = 'Grimm';
    return legendastv.search(searchTerm)
        .then(data => {
            expect(data).toHaveProperty("last_page", false);
            expect(data.releases).not.toBeNull()
            expect(data.releases.length).toBeGreaterThan(1);
            data.releases.forEach(release => {
                expect(release.name.toLowerCase()).toContain(searchTerm.toLowerCase());
            });
        });
});



test('results found should return non empty releases and have the search term in elements in page 2', () => {
    const searchTerm = 'Grimm';
    return legendastv.search(searchTerm, 2)
        .then(data => {
            expect(data).toHaveProperty("last_page", false);
            expect(data.releases).not.toBeNull()
            expect(data.releases.length).toBeGreaterThan(1);
            data.releases.forEach(release => {
                expect(release.name.toLowerCase()).toContain(searchTerm.toLowerCase());
            });
        });
});

test('autodetect should work, case 1', () => {
    return legendastv.autoDetect('Grimm.S06E12.720p.AMZN.WEBRip.DD5.1.x264-ViSUM')
        .then(data => {
            expect(data.name).toEqual('Grimm.S06E12.HDTV.x264-SVA-AFG-mSD-MeGusta-AVS-FUM-RMTeam-ViSUM-RARBG');
            expect(data.download).not.toBeNull()
        });
});

test('autodetect should work, case 2', () => {
    return legendastv.autoDetect('Grimm.S01E21.Big.Feet.1080i.HDTV.D5.1.MPEG2-TrollHD')
        .then(data => {
            expect(data.name).toEqual('Grimm.S01E21.Big.Feet.1080i.HDTV. D5.1.MPEG2-TrollHD');
            expect(data.download).not.toBeNull()
        });
});

test('autodetect should work, case 3', () => {
    return legendastv.autoDetect('Grimm.S01E21.720p.HDTV.X264-DIMENSION')
        .then(data => {
            expect(data.name).toEqual('Grimm.S01E21.HDTV.x264-LOL/DIMENSION/mSD/ECI');
            expect(data.download).not.toBeNull()
        });
});