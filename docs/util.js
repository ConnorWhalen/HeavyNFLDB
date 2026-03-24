
function playIcon(size) {
    return (
        `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">` +
            '<path d="M15 12.3301L9 16.6603L9 8L15 12.3301Z" fill="currentColor" />' +
        '</svg>'
    );
}

function closeIcon(size) {
    return (
        `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">` +
            '<path d="M6.2253 4.81108C5.83477 4.42056 5.20161 4.42056 4.81108 4.81108C4.42056 5.20161 4.42056 5.83477 4.81108 6.2253L10.5858 12L4.81114 17.7747C4.42062 18.1652 4.42062 18.7984 4.81114 19.1889C5.20167 19.5794 5.83483 19.5794 6.22535 19.1889L12 13.4142L17.7747 19.1889C18.1652 19.5794 18.7984 19.5794 19.1889 19.1889C19.5794 18.7984 19.5794 18.1652 19.1889 17.7747L13.4142 12L19.189 6.2253C19.5795 5.83477 19.5795 5.20161 19.189 4.81108C18.7985 4.42056 18.1653 4.42056 17.7748 4.81108L12 10.5858L6.2253 4.81108Z" fill="currentColor"/>' +
        '</svg>'
    );
}

function compNullsLast(a, b, comp) {
    if (a === null && b === null) {
        return 0;
    }
    if (a === null) {
        return 1;
    }
    if (b === null) {
        return -1;
    }
    return comp(a, b);
}

function compNegativesLast(a, b, comp) {
    if (a < 0 && b < 0) {
        return 0;
    }
    if (a < 0) {
        return 1;
    }
    if (b < 0) {
        return -1;
    }
    return comp(a, b);
}

function readableDate(isodate) {
    const dateObject = new Date(isodate);

    // Format using default locale (e.g., "May 25, 2025" in en-US)
    return dateObject.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}
