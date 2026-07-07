# -*- coding: utf-8 -*-
from classify import classify


def test_base_mapping_keeps_ordinary_slides():
    assert classify(1, "ELIZA and the history of chatbots") == ("keep", 1, "base mapping")
    assert classify(12, "Agentic code with Claude Code") == ("keep", 11, "base mapping")
    assert classify(15, "Claude Skills overview") == ("keep", 14, "base mapping")


def test_old_ten_and_eleven_both_map_to_new_ten():
    assert classify(10, "Building an AI app")[1] == 10
    assert classify(11, "Deploying with GitHub Pages")[1] == 10


def test_code_to_joy_cut_everywhere():
    action, target, reason = classify(9, "Code to Joy: The What of Programming")
    assert action == "cut" and target is None and "Littman" in reason


def test_oz_corpus_cut():
    assert classify(15, "Fine-tuning on the Wizard of Oz books")[0] == "cut"
    assert classify(15, "The Oz Completion Model results")[0] == "cut"


def test_eternauta_and_gemini_offer_cut():
    assert classify(7, "Netflix's El Eternauta and AI")[0] == "cut"
    assert classify(7, "Google's free year of Gemini for students")[0] == "cut"


def test_sora_kept_only_in_week_seven():
    action, target, reason = classify(7, "Sora: OpenAI's video model")
    assert (action, target) == ("keep", 7) and "case study" in reason
    assert classify(13, "Try Sora for video generation")[0] == "cut"


def test_noble_routes_by_source_deck():
    assert classify(9, "Noble, The Power of Algorithms") == (
        "move", 4, "Noble chapter now assigned in Week 4")
    assert classify(11, "Algorithms of Oppression: Searching for Black Girls")[:2] == ("move", 6)
    assert classify(14, "Noble on the future of knowledge")[:2] == ("move", 7)


def test_dropped_noble_chapters_cut():
    assert classify(12, "Noble: Searching for People and Communities")[0] == "cut"
    assert classify(13, "Noble: Searching for Protections")[0] == "cut"


def test_mitchell_routes_up_two_weeks():
    assert classify(3, "Melanie Mitchell, Part I: Background")[:2] == ("move", 1)
    assert classify(7, "Mitchell Part V: The Barrier of Meaning")[:2] == ("move", 5)


def test_cut_wins_over_move():
    # a slide mentioning both Littman and Noble is about the removed book pairing
    assert classify(9, "Code to Joy and Noble this week")[0] == "cut"
