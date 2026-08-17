#!/usr/bin/python3

from datetime import timedelta

from etv_client.models.content_smart_collection import ContentSmartCollection
from etv_client.models.content_collection import ContentCollection
from etv_client.models.playout_count import PlayoutCount
from etv_client.models.playout_pad_until_exact import PlayoutPadUntilExact
from etv_client.models.control_wait_until_exact import ControlWaitUntilExact
from etv_client.models.control_watermark_on import ControlWatermarkOn
from etv_client.models.control_watermark_off import ControlWatermarkOff
from etv_client.models.control_graphics_on import ControlGraphicsOn
from etv_client.models.control_graphics_off import ControlGraphicsOff
from etv_client.models.control_start_epg_group import ControlStartEpgGroup


# ---------------------------------------------------------
# WATERMARKS
# ---------------------------------------------------------

NORMAL_WATERMARK = "AdaMTV 90s Colour Logo"
HOUSE_WATERMARK = "AdaMTV 90's Colour House Classics Logo"
BRITPOP_WATERMARK = "AdaMTV 90's Colour Britpop Logo"
WATERMARK_1995 = "AdaMTV 90's Colour 1995 Logo"
WATERMARK_1996 = "AdaMTV 90's Colour 1996 Logo"


# ---------------------------------------------------------
# FEATURED ARTIST GRAPHICS
# ---------------------------------------------------------

BLUR_GRAPHIC = "text/featured-artist-blur.yml"
OASIS_GRAPHIC = "text/featured-artist-oasis.yml"
RADIOHEAD_GRAPHIC = "text/featured-artist-radiohead.yml"
AEROSMITH_GRAPHIC = "text/featured-artist-aerosmith.yml"
PRODIGY_GRAPHIC = "text/featured-artist-prodigy.yml"
GLASTONBURY_GRAPHIC = "text/glastonbury-mix.yml"

# ---------------------------------------------------------
# CUE DOT
# ---------------------------------------------------------

CUE_DOT_GRAPHIC = "motion/cue-dot.yml"

# ---------------------------------------------------------
# TIMING HELPERS
#
# These are the pieces that make the cycle land exactly on
# a boundary (e.g. 12:00:00, 19:00:00) instead of drifting
# past it. The key idea: check BEFORE committing an item,
# using peek_next, rather than committing it and checking
# afterwards. pad_until_exact / wait_until_exact only ever
# add content moving forward from "now" - once you've
# overshot "when", they can't retroactively claw time back.
# ---------------------------------------------------------

def seconds_until(context, boundary):
    """How much time is left before the boundary, in seconds.
    Negative or zero means we've already reached/passed it."""

    if boundary is None:
        return None

    return (boundary - context.current_time).total_seconds()


def peek_seconds(api, build_id, content_key):
    """Duration in seconds of whatever would play next from this
    content key, WITHOUT scheduling it."""

    peek = api.peek_next(build_id, content_key)
    return peek.milliseconds / 1000.0


def close_gap(api, build_id, boundary, prefer_content="ADS"):
    """Close the remaining gap up to `boundary` exactly, preferring
    to find whole, untrimmed content that happens to fit. Only
    trims as a last resort, and only trims `prefer_content`
    (adverts by default) - never a music video.

    Returns the updated context.
    """

    # First pass: look for content that already fits the gap
    # without cutting anything. discardAttempts gives ErsatzTV
    # several tries to find a naturally-fitting item/combination.
    context = api.pad_until_exact(
        build_id,
        PlayoutPadUntilExact(
            content=prefer_content,
            when=boundary,
            trim=False,
            discardAttempts=8,
            stopBeforeEnd=True
        )
    )

    # If nothing fit exactly, fall back to trimming the last
    # advert so we land on the boundary precisely no matter what.
    if context.current_time < boundary:
        context = api.pad_until_exact(
            build_id,
            PlayoutPadUntilExact(
                content=prefer_content,
                when=boundary,
                trim=True,
                stopBeforeEnd=True
            )
        )

    return context


# ---------------------------------------------------------
# CONTENT
# ---------------------------------------------------------

def define_content(api, context, build_id):

    # Main rotation
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="MAIN",
            smartCollection="All Music Videos",
            order="shuffle"
        )
    )

    # House Classics
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="HOUSE",
            smartCollection="House Classics",
            order="shuffle"
        )
    )

    # Britpop
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="BRITPOP",
            smartCollection="Britpop",
            order="shuffle"
        )
    )

    # Blur
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="BLUR",
            smartCollection="Blur",
            order="shuffle"
        )
    )

    # Oasis
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="OASIS",
            smartCollection="Oasis",
            order="shuffle"
        )
    )

    # Radiohead
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="RADIOHEAD",
            smartCollection="Radiohead",
            order="shuffle"
        )
    )

    # Aerosmith
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="AEROSMITH",
            smartCollection="Aerosmith",
            order="shuffle"
        )
    )

    # Prodigy
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="PRODIGY",
            smartCollection="Prodigy",
            order="shuffle"
        )
    )

    # 1995 Music Videos
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="SPECIAL1995",
            smartCollection="1995 Music Videos",
            order="shuffle"
        )
    )

    # 1996 Music Videos
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="SPECIAL1996",
            smartCollection="1996 Music Videos",
            order="shuffle"
        )
    )

    # Manual collections
    api.add_collection(
        build_id,
        ContentCollection(
            key="BRB",
            collection="We'll Be Right Back",
            order="shuffle"
        )
    )

    api.add_collection(
        build_id,
        ContentCollection(
            key="ADS",
            collection="All Commercials",
            order="shuffle"
        )
    )

    api.add_collection(
        build_id,
        ContentCollection(
            key="BACK",
            collection="We Are Back",
            order="shuffle"
        )
    )

    # Smart collection containing the Glastonbury Classics music videos.
    api.add_smart_collection(
    	build_id,
    	ContentSmartCollection(
            key="GLASTONBURY",
            smartCollection="Glastonbury Music Videos",
            order="shuffle"
    	)
    )

    # Intro bumper played once at the start of the Oasis special,
    # before the video cycles begin.
    api.add_collection(
        build_id,
        ContentCollection(
            key="OASIS_INTRO",
            collection="Oasis Special Intro",
            order="shuffle"
        )
    )

    # Intro bumper played once at the start of the Blur special,
    # before the video cycles begin.
    api.add_collection(
        build_id,
        ContentCollection(
            key="BLUR_INTRO",
            collection="Blur Special Intro",
            order="shuffle"
        )
    )

    # Intro bumper played once at the start of the Radiohead
    # special, before the video cycles begin.
    api.add_collection(
        build_id,
        ContentCollection(
            key="RADIOHEAD_INTRO",
            collection="Radiohead Special Intro",
            order="shuffle"
        )
    )

    # Intro bumper played once at the start of the Aerosmith
    # special, before the video cycles begin.
    api.add_collection(
        build_id,
        ContentCollection(
            key="AEROSMITH_INTRO",
            collection="Aerosmith Special Intro",
            order="shuffle"
        )
    )

    # Intro bumper played once at the start of the Prodigy
    # special, before the video cycles begin.
    api.add_collection(
        build_id,
        ContentCollection(
            key="PRODIGY_INTRO",
            collection="Prodigy Special Intro",
            order="shuffle"
        )
    )

    # Intro bumper played once at the start of the Glastonbury
    # Classics special, before the video cycles begin.
    api.add_collection(
        build_id,
        ContentCollection(
            key="GLASTONBURY_INTRO",
            collection="Glastonbury Classics Intro",
            order="shuffle"
        )
    )

    # Intro bumper played once at the start of each Non-Stop 90s
    # normal programming block (i.e. every time it resumes after
    # a special finishes), before the video cycles begin.
    api.add_collection(
        build_id,
        ContentCollection(
            key="NONSTOP_INTRO",
            collection="Non-Stop 90s Intro",
            order="shuffle"
        )
    )


def reset_playout(api, context, build_id):
    return context


# ---------------------------------------------------------
# STANDARD CYCLE
#
# 3 music videos -> BRB bumper -> 2 adverts -> BACK bumper.
#
# `boundary`, if given, is the exact time this cycle must not
# run past (e.g. a special's start time). When set:
#   - each video is peeked before being committed; a video
#     that wouldn't fit is simply not started (it plays next
#     cycle instead) - videos are NEVER trimmed.
#   - the BRB bumper is skipped if there isn't room for it.
#   - the ad break is closed exactly on the boundary via
#     close_gap(), which trims an advert only if nothing else
#     fits - the BACK bumper is skipped in this case, since
#     the special takes over immediately after the ads.
# ---------------------------------------------------------

def add_cycle(api, context, build_id, content, story=False, boundary=None):

    videos_played = 0
    ran_short = False  # a video didn't fit - we're near the boundary

    for _ in range(3):

        if boundary is not None:
            remaining = seconds_until(context, boundary)
            if remaining <= 0:
                return context, videos_played

            next_dur = peek_seconds(api, build_id, content)
            if next_dur > remaining:
                # Doesn't fit - stop here, don't start this video.
                ran_short = True
                break

        turn_graphic_on(api, build_id, "motion/adamtv-now-playing-final.yml")
        turn_graphic_on(api, build_id, "text/adamtv-now-playing.yml")
        turn_graphic_on(api, build_id, "text/adamtv-now-playing-end.yml")

        if story:
            turn_graphic_on(api, build_id, "text/story-behind-the-song.yml")

        # The third video also gets the ITV-style cue dot, which
        # starts 10 seconds before this video's end according to
        # the motion graphic YAML.
        if videos_played == 2:
            turn_graphic_on(api, build_id, CUE_DOT_GRAPHIC)

        context = api.add_count(
            build_id,
            PlayoutCount(content=content, count=1)
        )

        if videos_played == 2:
            turn_graphic_off(api, build_id, CUE_DOT_GRAPHIC)

        turn_graphic_off(api, build_id, "motion/adamtv-now-playing-final.yml")
        turn_graphic_off(api, build_id, "text/adamtv-now-playing.yml")
        turn_graphic_off(api, build_id, "text/adamtv-now-playing-end.yml")

        if story:
            turn_graphic_off(api, build_id, "text/story-behind-the-song.yml")

        videos_played += 1

    # -------------------------------------------------
    # BREAK: BRB bumper -> adverts -> BACK bumper
    #
    # IMPORTANT: the "close the gap without trimming a video,
    # trim an advert as a last resort" logic below is ONLY used
    # on the cycle that actually runs into the boundary. Every
    # other cycle gets the plain fixed break, exactly as before -
    # otherwise pad_until_exact ends up filling hours of airtime
    # with nothing but adverts, which is what just bit us.
    # -------------------------------------------------

    if videos_played == 0 and not ran_short:
        # Nothing fit and we're not near a boundary either -
        # shouldn't normally happen, but bail out safely.
        return context, 0

    if ran_short:
        remaining = seconds_until(context, boundary)
        if remaining > 0:
            brb_dur = peek_seconds(api, build_id, "BRB")
            if brb_dur <= remaining:
                context = api.add_count(build_id, PlayoutCount(content="BRB", count=1))
            context = close_gap(api, build_id, boundary, prefer_content="ADS")
        return context, videos_played

    if boundary is not None:
        remaining = seconds_until(context, boundary)
        if remaining <= 0:
            return context, videos_played

        brb_dur = peek_seconds(api, build_id, "BRB")
        ad_dur = peek_seconds(api, build_id, "ADS")
        back_dur = peek_seconds(api, build_id, "BACK")
        estimated_break = brb_dur + (2 * ad_dur) + back_dur

        if estimated_break > remaining:
            # The full break itself wouldn't fit before the
            # boundary - close the gap instead of forcing it.
            if brb_dur <= remaining:
                context = api.add_count(build_id, PlayoutCount(content="BRB", count=1))
            context = close_gap(api, build_id, boundary, prefer_content="ADS")
            return context, videos_played

    # Comfortably fits (or there's no boundary at all) - normal break.
    context = api.add_count(build_id, PlayoutCount(content="BRB", count=1))
    context = api.add_count(build_id, PlayoutCount(content="ADS", count=2))
    context = api.add_count(build_id, PlayoutCount(content="BACK", count=1))

    return context, videos_played


# ---------------------------------------------------------
# WEEKLY SPECIALS
#
# weekday:
# Monday = 0
# Tuesday = 1
# Wednesday = 2
# Thursday = 3
# Friday = 4
# Saturday = 5
# Sunday = 6
# ---------------------------------------------------------

def get_week_start(now):

    return (
        now
        - timedelta(days=now.weekday())
    ).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )


def get_weekly_events(now):

    week = get_week_start(now)

    events = [

        # Monday 12:00-14:00
        (
            week + timedelta(days=0, hours=12),
            week + timedelta(days=0, hours=14),
            "The Story Behind the Song",
            "MAIN",
            NORMAL_WATERMARK,
            None,
            True,
            None  # intro bumper (content key) - None means no intro
        ),

        # Tuesday 12:00-14:00
        (
            week + timedelta(days=1, hours=12),
            week + timedelta(days=1, hours=14),
            "The Story Behind the Song",
            "MAIN",
            NORMAL_WATERMARK,
            None,
            True,
            None  # intro bumper (content key) - None means no intro
        ),

        # Wednesday 12:00-14:00
        (
            week + timedelta(days=2, hours=12),
            week + timedelta(days=2, hours=14),
            "The Story Behind the Song",
            "MAIN",
            NORMAL_WATERMARK,
            None,
            True,
            None  # intro bumper (content key) - None means no intro
        ),

        # Thursday 12:00-14:00
        (
            week + timedelta(days=3, hours=12),
            week + timedelta(days=3, hours=14),
            "The Story Behind the Song",
            "MAIN",
            NORMAL_WATERMARK,
            None,
            True,
            None  # intro bumper (content key) - None means no intro
        ),

        # Friday 12:00-14:00
        (
            week + timedelta(days=4, hours=12),
            week + timedelta(days=4, hours=14),
            "The Story Behind the Song",
            "MAIN",
            NORMAL_WATERMARK,
            None,
            True,
            None  # intro bumper (content key) - None means no intro
        ),

        # Monday 19:00-20:00
        (
            week + timedelta(days=0, hours=19),
            week + timedelta(days=0, hours=20),
            "Glastonbury Classics",
            "GLASTONBURY",
            NORMAL_WATERMARK,
            GLASTONBURY_GRAPHIC,
            False,
            "GLASTONBURY_INTRO"  # plays once before the video cycles begin
        ),

        # Tuesday 19:00-20:00
        (
            week + timedelta(days=1, hours=19),
            week + timedelta(days=1, hours=20),
            "Feature Hour: 1996",
            "SPECIAL1996",
            WATERMARK_1996,
            None,
            False,
            None  # intro bumper (content key) - None means no intro
        ),

        # Wednesday 19:00-20:00
        (
            week + timedelta(days=2, hours=19),
            week + timedelta(days=2, hours=20),
            "Feature Hour: 1995",
            "SPECIAL1995",
            WATERMARK_1995,
            None,
            False,
            None  # intro bumper (content key) - None means no intro
        ),

        # Friday 19:00-21:00
        (
            week + timedelta(days=4, hours=19),
            week + timedelta(days=4, hours=21),
            "House Classics",
            "HOUSE",
            HOUSE_WATERMARK,
            None,
            False,
            None  # intro bumper (content key) - None means no intro
        ),

        # Saturday 11:00-12:00
        (
            week + timedelta(days=5, hours=11),
            week + timedelta(days=5, hours=12),
            "Featured Artist: Aerosmith",
            "AEROSMITH",
            NORMAL_WATERMARK,
            AEROSMITH_GRAPHIC,
            False,
            "AEROSMITH_INTRO"  # plays once before the video cycles begin
        ),

        # Saturday 12:00-18:00
        (
            week + timedelta(days=5, hours=12),
            week + timedelta(days=5, hours=18),
            "Britpop",
            "BRITPOP",
            BRITPOP_WATERMARK,
            None,
            False,
            None  # intro bumper (content key) - None means no intro
        ),

        # Saturday 18:00-19:00
        (
            week + timedelta(days=5, hours=18),
            week + timedelta(days=5, hours=19),
            "Featured Artist: Prodigy",
            "PRODIGY",
            NORMAL_WATERMARK,
            PRODIGY_GRAPHIC,
            False,
            "PRODIGY_INTRO"  # plays once before the video cycles begin
        ),

        # Sunday 12:00-13:00
        (
            week + timedelta(days=6, hours=12),
            week + timedelta(days=6, hours=13),
            "Featured Artist: Radiohead",
            "RADIOHEAD",
            NORMAL_WATERMARK,
            RADIOHEAD_GRAPHIC,
            False,
            "RADIOHEAD_INTRO"  # plays once before the video cycles begin
        ),

        # Sunday 15:00-16:00
        (
            week + timedelta(days=6, hours=15),
            week + timedelta(days=6, hours=16),
            "Featured Artist: Blur",
            "BLUR",
            NORMAL_WATERMARK,
            BLUR_GRAPHIC,
            False,
            "BLUR_INTRO"  # plays once before the video cycles begin
        ),

        # Sunday 16:00-17:00
        (
            week + timedelta(days=6, hours=16),
            week + timedelta(days=6, hours=17),
            "Featured Artist: Oasis",
            "OASIS",
            NORMAL_WATERMARK,
            OASIS_GRAPHIC,
            False,
            "OASIS_INTRO"  # plays once before the video cycles begin
        )
    ]

    return events


def find_next_special(now):

    events = get_weekly_events(now)

    # If we're currently inside a special, return it.
    for event in events:

        start, end, name, content, watermark, graphic, story, intro = event

        if start <= now < end:
            return event

    # Otherwise find the next event - sorted by start time, so the
    # order events are defined in above no longer matters.
    future_events = sorted(
        (event for event in events if event[0] > now),
        key=lambda event: event[0]
    )

    if future_events:
        return future_events[0]

    # We've passed all this week's events.
    # Build next week's events.
    next_week = now + timedelta(days=7)

    return sorted(get_weekly_events(next_week), key=lambda event: event[0])[0]


# ---------------------------------------------------------
# WATERMARK / GRAPHICS / EPG
# ---------------------------------------------------------

def set_watermark(api, build_id, watermark):

    api.watermark_off(
        build_id,
        ControlWatermarkOff()
    )

    api.watermark_on(
        build_id,
        ControlWatermarkOn(
            watermark=[watermark]
        )
    )


def turn_graphic_on(api, build_id, graphic):

    if graphic:

        api.graphics_on(
            build_id,
            ControlGraphicsOn(
                graphics=[graphic]
            )
        )


def turn_graphic_off(api, build_id, graphic):

    if graphic:

        api.graphics_off(
            build_id,
            ControlGraphicsOff(
                graphics=[graphic]
            )
        )


def start_epg_group(api, build_id, title):

    api.start_epg_group(
        build_id,
        ControlStartEpgGroup(
            advance=True,
            customTitle=title
        )
    )


def stop_epg_group(api, build_id):

    api.stop_epg_group(build_id)


# ---------------------------------------------------------
# BUILD A SPECIAL
# ---------------------------------------------------------

def build_special(
    api,
    context,
    build_id,
    start,
    end,
    name,
    content,
    watermark,
    graphic,
    story,
    intro=None
):

    # Start EPG programme
    start_epg_group(
        api,
        build_id,
        name
    )

    # Switch watermark
    set_watermark(
        api,
        build_id,
        watermark
    )

    # Play the intro bumper once, before anything else - only if
    # it still fits before `end` (matters for very short specials).
    if intro and context.current_time < end:
        context = api.add_count(
            build_id,
            PlayoutCount(content=intro, count=1)
        )

    # Turn on featured artist graphic if required
    turn_graphic_on(
        api,
        build_id,
        graphic
    )

    # Fill the special with normal cycles, landing exactly on `end`.
    while (
        not context.is_done
        and context.current_time < end
    ):

        previous_time = context.current_time

        context, videos_played = add_cycle(
            api,
            context,
            build_id,
            content,
            story=story,
            boundary=end
        )

        if context.current_time >= end:
            break

        # Safety: nothing was added and we're still short of the
        # boundary - avoid looping forever.
        if context.current_time <= previous_time or videos_played == 0:
            break

    # If we still fell short of `end` (e.g. the safety break above
    # fired), close the remaining gap exactly.
    if context.current_time < end:
        context = close_gap(api, build_id, end, prefer_content="ADS")

    # Turn off featured graphic
    turn_graphic_off(
        api,
        build_id,
        graphic
    )

    # Return to normal watermark
    set_watermark(
        api,
        build_id,
        NORMAL_WATERMARK
    )

    # Finish EPG programme
    stop_epg_group(
        api,
        build_id
    )

    return context


# ---------------------------------------------------------
# MAIN PLAYOUT BUILDER
# ---------------------------------------------------------

def build_playout(api, context, build_id):

    while not context.is_done:

        now = context.current_time

        (
            special_start,
            special_end,
            special_name,
            special_content,
            special_watermark,
            special_graphic,
            special_story,
            special_intro
        ) = find_next_special(now)

        # -------------------------------------------------
        # NORMAL PROGRAMMING BEFORE NEXT SPECIAL
        # -------------------------------------------------

        if now < special_start:

            # Start normal EPG programme
            start_epg_group(
                api,
                build_id,
                "Non-stop 90s"
            )

            # Play the intro bumper once, before the video cycles
            # begin - only if it still fits before the next special.
            if context.current_time < special_start:
                context = api.add_count(
                    build_id,
                    PlayoutCount(content="NONSTOP_INTRO", count=1)
                )

            while (
                not context.is_done
                and context.current_time < special_start
            ):

                previous_time = context.current_time

                context, videos_played = add_cycle(
                    api,
                    context,
                    build_id,
                    "MAIN",
                    boundary=special_start
                )

                if context.current_time >= special_start:
                    break

                if context.current_time <= previous_time or videos_played == 0:
                    break

            # Finish normal EPG programme
            stop_epg_group(
                api,
                build_id
            )

            if context.is_done:
                break

            # If there is still a gap, wait exactly until
            # the special begins.
            if context.current_time < special_start:

                context = api.wait_until_exact(
                    build_id,
                    ControlWaitUntilExact(
                        when=special_start,
                        rewindOnReset=False
                    )
                )

        if context.is_done:
            break

        # -------------------------------------------------
        # SPECIAL
        # -------------------------------------------------

        context = build_special(
            api,
            context,
            build_id,
            special_start,
            special_end,
            special_name,
            special_content,
            special_watermark,
            special_graphic,
            special_story,
            intro=special_intro
        )

    return context
