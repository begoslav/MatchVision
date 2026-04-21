"""Summary generation service for match summaries"""
import logging
import random

logger = logging.getLogger(__name__)


def _int(val):
    if val is None:
        return 0
    try:
        return int(str(val).replace('%', '') or 0)
    except (ValueError, TypeError):
        return 0


class SummaryService:
    """Service for generating rich match summaries from statistics and events"""

    @staticmethod
    def generate_match_summary(match_data: dict) -> str:
        """Generate a detailed match summary from all available data."""
        try:
            home_team = match_data.get('teams', {}).get('home', {}).get('name', 'Domácí')
            away_team = match_data.get('teams', {}).get('away', {}).get('name', 'Hosté')
            home_score = _int(match_data.get('goals', {}).get('home', 0))
            away_score = _int(match_data.get('goals', {}).get('away', 0))
            status = match_data.get('fixture', {}).get('status', {}).get('short', 'FT')

            statistics = match_data.get('statistics', [])
            home_stats = {s['type']: s['value'] for s in (statistics[0].get('statistics', []) if statistics else [])}
            away_stats = {s['type']: s['value'] for s in (statistics[1].get('statistics', []) if len(statistics) > 1 else [])}

            home_shots     = _int(home_stats.get('Total Shots', 0))
            away_shots     = _int(away_stats.get('Total Shots', 0))
            home_on_target = _int(home_stats.get('Shots on Goal', 0))
            away_on_target = _int(away_stats.get('Shots on Goal', 0))
            home_poss      = _int(home_stats.get('Ball Possession', 0))
            away_poss      = _int(away_stats.get('Ball Possession', 0))
            home_saves     = _int(home_stats.get('Goalkeeper Saves', 0))
            away_saves     = _int(away_stats.get('Goalkeeper Saves', 0))
            home_fouls     = _int(home_stats.get('Fouls', 0))
            away_fouls     = _int(away_stats.get('Fouls', 0))
            home_corners   = _int(home_stats.get('Corner Kicks', 0))
            away_corners   = _int(away_stats.get('Corner Kicks', 0))
            home_yellow    = _int(home_stats.get('Yellow Cards', 0))
            away_yellow    = _int(away_stats.get('Yellow Cards', 0))
            home_red       = _int(home_stats.get('Red Cards', 0))
            away_red       = _int(away_stats.get('Red Cards', 0))

            events     = match_data.get('events', [])
            goal_events = [e for e in events if e.get('type') == 'Goal' and e.get('detail') != 'Missed Penalty']
            red_events  = [e for e in events if e.get('type') == 'Card' and e.get('detail') in ('Red Card', 'Second Yellow card')]
            sub_events  = [e for e in events if e.get('type') == 'subst']

            parts = []

            if status not in ('FT', 'AET', 'PEN', 'AWD', 'WO'):
                parts.append(f"Zápas ještě neskončil (stav: {status}).")

            score_str = f"{home_score}:{away_score}"
            if home_score > away_score:
                diff = home_score - away_score
                if diff >= 3:
                    opener = random.choice([
                        f"{home_team} deklasovala {away_team} {score_str}.",
                        f"Jednoznačná záležitost – {home_team} rozdrtila {away_team} {score_str}.",
                    ])
                elif diff == 2:
                    opener = random.choice([
                        f"{home_team} přesvědčivě zdolala {away_team} {score_str}.",
                        f"Solidní vítězství {home_team} {score_str} nad {away_team}.",
                    ])
                else:
                    opener = random.choice([
                        f"{home_team} těsně porazila {away_team} {score_str}.",
                        f"Minimální rozdíl rozhodl – {home_team} vítězí {score_str} nad {away_team}.",
                    ])
            elif away_score > home_score:
                diff = away_score - home_score
                if diff >= 3:
                    opener = random.choice([
                        f"Překvapení! {away_team} deklasovala {home_team} {score_str} na jeho hřišti.",
                        f"{away_team} vyhrála přesvědčivě {score_str} na půdě {home_team}.",
                    ])
                elif diff == 2:
                    opener = f"{away_team} přesvědčivě zvítězila na hřišti {home_team} {score_str}."
                else:
                    opener = random.choice([
                        f"Těsná výhra hostů – {away_team} odvezla ze hřiště {home_team} tři body {score_str}.",
                        f"{away_team} si v dramatickém utkání poradila s {home_team} {score_str}.",
                    ])
            else:
                opener = random.choice([
                    f"{home_team} a {away_team} se dělí o bod po výsledku {score_str}.",
                    f"Zápas {home_team} vs {away_team} skončil remízou {score_str}.",
                ])
            parts.append(opener)

            if goal_events:
                scorer_parts = []
                for ev in goal_events:
                    player = ev.get('player', {}).get('name', '')
                    minute = ev.get('time', {}).get('elapsed', '?')
                    detail = ev.get('detail', '')
                    label = f"{player} ({minute}')" if player else f"({minute}')"
                    if detail == 'Own Goal':
                        label += ' (vlastní)'
                    elif detail == 'Penalty':
                        label += ' (PK)'
                    scorer_parts.append(label)
                parts.append(f"Góly: {', '.join(scorer_parts)}.")

            has_stats = home_shots > 0 or away_shots > 0 or home_poss > 0
            if has_stats:
                if home_poss and away_poss:
                    dom_team = home_team if home_poss >= away_poss else away_team
                    dom_poss = max(home_poss, away_poss)
                    if dom_poss >= 60:
                        parts.append(f"{dom_team} dominovala s míčem – {dom_poss}% držení.")
                    elif dom_poss >= 53:
                        parts.append(f"{dom_team} měla mírnou převahu s míčem ({dom_poss}%).")

                if home_shots and away_shots:
                    if home_on_target and away_on_target:
                        parts.append(
                            f"Střelecky: {home_team} {home_shots} střel ({home_on_target} na branku), "
                            f"{away_team} {away_shots} ({away_on_target} na branku)."
                        )
                    else:
                        parts.append(f"Střely: {home_team} {home_shots}, {away_team} {away_shots}.")

            if home_saves >= 5:
                parts.append(f"Brankář {home_team} si připsal {home_saves} zákroků a výrazně přispěl k výsledku.")
            elif away_saves >= 5:
                parts.append(f"Brankář {away_team} předvedl {away_saves} zákroků a udržoval svůj tým ve hře.")

            card_parts = []
            if home_red:
                names = [e['player']['name'] for e in red_events if e.get('team', {}).get('name') == home_team and e.get('player', {}).get('name')]
                label = f"{home_team} hrála v oslabení" + (f" po vyloučení {', '.join(names)}" if names else "")
                card_parts.append(label)
            if away_red:
                names = [e['player']['name'] for e in red_events if e.get('team', {}).get('name') == away_team and e.get('player', {}).get('name')]
                label = f"{away_team} hrála v oslabení" + (f" po vyloučení {', '.join(names)}" if names else "")
                card_parts.append(label)
            if card_parts:
                parts.append('. '.join(card_parts) + '.')

            if home_yellow + away_yellow >= 6:
                parts.append(
                    f"Tvrdý zápas – celkem {home_yellow + away_yellow} žlutých karet "
                    f"({home_team}: {home_yellow}, {away_team}: {away_yellow})."
                )

            if home_fouls + away_fouls >= 25:
                parts.append(f"Hodně faulů – domácí {home_fouls}, hosté {away_fouls}.")

            if home_corners + away_corners >= 10:
                parts.append(f"Rohové kopy: {home_team} {home_corners}, {away_team} {away_corners}.")

            if sub_events:
                home_subs = sum(1 for e in sub_events if e.get('team', {}).get('name') == home_team)
                away_subs = sum(1 for e in sub_events if e.get('team', {}).get('name') == away_team)
                if home_subs + away_subs > 0:
                    parts.append(f"Střídání: {home_team} {home_subs}×, {away_team} {away_subs}×.")

            if len(parts) <= 1:
                parts.append("Podrobné statistiky a sestavy najdete níže.")

            return ' '.join(parts)

        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Zápas byl odehrán. Podrobné statistiky najdete níže."

    @staticmethod
    def generate_team_form_summary(last_matches: list) -> dict:
        """Generate team form summary from last matches"""
        if not last_matches:
            return {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}

        stats = {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
        for match in last_matches[:5]:
            try:
                home_score = _int(match.get('goals', {}).get('home', 0))
                away_score = _int(match.get('goals', {}).get('away', 0))
                team_is_home = match.get('teams', {}).get('home', {}).get('id')
                if home_score > away_score:
                    if team_is_home:
                        stats['wins'] += 1; stats['goals_for'] += home_score; stats['goals_against'] += away_score
                    else:
                        stats['losses'] += 1; stats['goals_for'] += away_score; stats['goals_against'] += home_score
                elif home_score < away_score:
                    if team_is_home:
                        stats['losses'] += 1; stats['goals_for'] += home_score; stats['goals_against'] += away_score
                    else:
                        stats['wins'] += 1; stats['goals_for'] += away_score; stats['goals_against'] += home_score
                else:
                    stats['draws'] += 1; stats['goals_for'] += home_score; stats['goals_against'] += away_score
            except Exception as e:
                logger.error(f"Error processing match: {str(e)}")
        return stats


# Create singleton instance
summary_service = SummaryService()
