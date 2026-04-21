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


def _float(val):
    if val is None:
        return 0.0
    try:
        return float(str(val).replace('%', '') or 0)
    except (ValueError, TypeError):
        return 0.0


class SummaryService:
    """Service for generating match summaries from statistics and events"""

    @staticmethod
    def generate_match_summary(match_data: dict) -> str:
        """Generate a rich, detailed match summary from all available data."""
        try:
            home_team = match_data.get('teams', {}).get('home', {}).get('name', 'Domácí')
            away_team = match_data.get('teams', {}).get('away', {}).get('name', 'Hosté')
            home_score = _int(match_data.get('goals', {}).get('home', 0))
            away_score = _int(match_data.get('goals', {}).get('away', 0))
            status = match_data.get('fixture', {}).get('status', {}).get('short', 'FT')

            # Stats
            statistics = match_data.get('statistics', [])
            home_stats = {s['type']: s['value'] for s in (statistics[0].get('statistics', []) if statistics else [])}
            away_stats = {s['type']: s['value'] for s in (statistics[1].get('statistics', []) if len(statistics) > 1 else [])}

            home_shots      = _int(home_stats.get('Total Shots', 0))
            away_shots      = _int(away_stats.get('Total Shots', 0))
            home_on_target  = _int(home_stats.get('Shots on Goal', 0))
            away_on_target  = _int(away_stats.get('Shots on Goal', 0))
            home_poss       = _int(home_stats.get('Ball Possession', 0))
            away_poss       = _int(away_stats.get('Ball Possession', 0))
            home_saves      = _int(home_stats.get('Goalkeeper Saves', 0))
            away_saves      = _int(away_stats.get('Goalkeeper Saves', 0))
            home_fouls      = _int(home_stats.get('Fouls', 0))
            away_fouls      = _int(away_stats.get('Fouls', 0))
            home_corners    = _int(home_stats.get('Corner Kicks', 0))
            away_corners    = _int(away_stats.get('Corner Kicks', 0))
            home_yellow     = _int(home_stats.get('Yellow Cards', 0))
            away_yellow     = _int(away_stats.get('Yellow Cards', 0))
            home_red        = _int(home_stats.get('Red Cards', 0))
            away_red        = _int(away_stats.get('Red Cards', 0))

            # Events
            events = match_data.get('events', [])
            goal_events   = [e for e in events if e.get('type') == 'Goal' and e.get('detail') != 'Missed Penalty']
            red_events    = [e for e in events if e.get('type') == 'Card' and e.get('detail') in ('Red Card', 'Second Yellow card')]
            sub_events    = [e for e in events if e.get('type') == 'subst']

            parts = []

            # 1. Match status note for non-finished matches
            if status not in ('FT', 'AET', 'PEN', 'AWD', 'WO'):
                parts.append(f"Zápas ještě neskončil (stav: {status}).")

            # 2. Opening sentence – result
            score_str = f"{home_score}:{away_score}"
            if home_score > away_score:
                diff = home_score - away_score
                if diff >= 3:
                    opener = random.choice([
                        f"{home_team} deklasovala {away_team} {score_str}.",
                        f"Jednoznačná záležitost – {home_team} rozdrtila {away_team} {score_str}.",
                        f"Bezprecedentní výhra {home_team} nad {away_team} {score_str}.",
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
                    opener = random.choice([
                        f"{away_team} přesvědčivě zvítězila na hřišti {home_team} {score_str}.",
                        f"Cenné vítězství hostů – {away_team} bere tři body {score_str}.",
                    ])
                else:
                    opener = random.choice([
                        f"Těsná výhra hostů – {away_team} odvezla ze hřiště {home_team} tři body {score_str}.",
                        f"{away_team} si v dramatickém utkání dokázala poradit s {home_team} {score_str}.",
                    ])
            else:
                opener = random.choice([
                    f"Bezgólová remíza? Ne, {home_team} a {away_team} se dělí o bod po výsledku {score_str}.",
                    f"Zápas {home_team} vs {away_team} skončil remízou {score_str}.",
                    f"Body se dělí – {home_team} a {away_team} remizovaly {score_str}.",
                ])
            parts.append(opener)

            # 3. Goalscorers
            if goal_events:
                scorer_parts = []
                for ev in goal_events:
                    player = ev.get('player', {}).get('name', '')
                    minute = ev.get('time', {}).get('elapsed', '?')
                    detail = ev.get('detail', '')
                    team_name = ev.get('team', {}).get('name', '')
                    label = f"{player} ({minute}')"
                    if detail == 'Own Goal':
                        label += ' (vlastní)'
                    elif detail == 'Penalty':
                        label += ' (PK)'
                    if player:
                        scorer_parts.append(label)
                if scorer_parts:
                    parts.append(f"Góly: {', '.join(scorer_parts)}.")

            # 4. Possession & shots analysis
            has_stats = home_shots > 0 or away_shots > 0 or home_poss > 0
            if has_stats:
                if home_poss and away_poss:
                    dom_team = home_team if home_poss > away_poss else away_team
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

            # 5. Goalkeeper highlight
            if home_saves >= 5:
                parts.append(f"Brankář {home_team} si připsal {home_saves} zákroků a výrazně přispěl k výsledku.")
            elif away_saves >= 5:
                parts.append(f"Brankář {away_team} předvedl {away_saves} zákroků a udržoval svůj tým ve hře.")

            # 6. Cards / discipline
            card_parts = []
            if home_red:
                reds = [e for e in red_events if e.get('team', {}).get('name') == home_team]
                names = [e['player']['name'] for e in reds if e.get('player', {}).get('name')]
                label = f"{home_team} hrála v oslabení" + (f" po vyloučení {', '.join(names)}" if names else "")
                card_parts.append(label)
            if away_red:
                reds = [e for e in red_events if e.get('team', {}).get('name') == away_team]
                names = [e['player']['name'] for e in reds if e.get('player', {}).get('name')]
                label = f"{away_team} hrála v oslabení" + (f" po vyloučení {', '.join(names)}" if names else "")
                card_parts.append(label)
            if card_parts:
                parts.append('. '.join(card_parts) + '.')

            if home_yellow + away_yellow >= 6:
                parts.append(
                    f"Tvrdý zápas – celkem {home_yellow + away_yellow} žlutých karet "
                    f"({home_team}: {home_yellow}, {away_team}: {away_yellow})."
                )

            # 7. Fouls
            if home_fouls + away_fouls >= 25:
                parts.append(f"Hodně faulů – domácí {home_fouls}, hosté {away_fouls}.")

            # 8. Corners
            if home_corners + away_corners >= 10:
                parts.append(f"Rohové kopy: {home_team} {home_corners}, {away_team} {away_corners}.")

            # 9. Substitutions summary (count only)
            if sub_events:
                home_subs = sum(1 for e in sub_events if e.get('team', {}).get('name') == home_team)
                away_subs = sum(1 for e in sub_events if e.get('team', {}).get('name') == away_team)
                if home_subs + away_subs > 0:
                    parts.append(f"Střídání: {home_team} {home_subs}×, {away_team} {away_subs}×.")

            # 10. Fallback
            if len(parts) <= 1:
                parts.append("Podrobné statistiky a sestavy najdete níže.")

            return ' '.join(parts)

        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Zápas byl odehrán. Podrobné statistiky najdete níže."

    @staticmethod
    def generate_team_form_summary(last_matches: list) -> dict:
        """Generate team form summary from last matches"""
        if not last_matches or len(last_matches) == 0:
            return {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}

        stats = {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}

        for match in last_matches[:5]:
            try:
                home_score = _int(match.get('goals', {}).get('home', 0))
                away_score = _int(match.get('goals', {}).get('away', 0))
                team_is_home = match.get('teams', {}).get('home', {}).get('id')

                if home_score > away_score:
                    if team_is_home:
                        stats['wins'] += 1
                        stats['goals_for'] += home_score
                        stats['goals_against'] += away_score
                    else:
                        stats['losses'] += 1
                        stats['goals_for'] += away_score
                        stats['goals_against'] += home_score
                elif home_score < away_score:
                    if team_is_home:
                        stats['losses'] += 1
                        stats['goals_for'] += home_score
                        stats['goals_against'] += away_score
                    else:
                        stats['wins'] += 1
                        stats['goals_for'] += away_score
                        stats['goals_against'] += home_score
                else:
                    stats['draws'] += 1
                    stats['goals_for'] += home_score
                    stats['goals_against'] += away_score
            except Exception as e:
                logger.error(f"Error processing match: {str(e)}")
                continue

        return stats


# Create singleton instance
summary_service = SummaryService()


class SummaryService:
    """Service for generating match summaries from statistics"""
    
    SUMMARY_TEMPLATES = {
        'dominant_win': [
            "Naprostá dominance {home_team}. {away_team} neměla šanci. Střely {home_shots}:{away_shots}, držení míče {home_possession}:{away_possession}%.",
            "{home_team} zcela přehrála {away_team}. Jasné vítězství s třemi góly rozdílu a výraznou převahou.",
            "Bez diskuse {home_team}. Efektivita střel a dominance ve všech aspektech hry. {away_team} rezignovala.",
        ],
        'narrow_win': [
            "{home_team} vítězí těsně 1:0 po dramatickém zápase. {away_team} si vytvořila příležitosti, ale chybělo konkrétní zakončení.",
            "Tesný výsledek rozhoduje jeden gól. {home_team} byla efektivnější před bránou. Zápas byl vyrovnaný, ale {home_team} si výhru zasloužila.",
            "Minimální marže vítězství pro {home_team}. Vyrovnný zápas rozhodla kvalita v útoku. {away_team} měla možnosti, ale neurvala je.",
        ],
        'draw': [
            "Vyrovnaný souboj bez vítěze. Obě mužstva si vytvořila příležitosti, ale jejich realizace se nepovedla. Spravedlivý результат.",
            "{home_team} a {away_team} se rozdělily o body. Zajímavý zápas s příležitostmi na obou stranách.",
            "Bez ideálního zakončení se zápas skončil v remíze. Oba týmy měly své příležitosti, ale střelecky nebyli přesní.",
        ],
        'home_loss': [
            "Překvapení! {away_team} zvítězila na hřišti {home_team}. Rozhodla kvalita v útoku a lépe využité příležitosti.",
            "Zklamání pro {home_team}. {away_team} se prosadila také díky slabší obraně domácích.",
            "{away_team} si odvážela vítězství. {home_team} nebyla dostatečně efektivní a defenzíva se zapomněla.",
        ]
    }
    
    @staticmethod
    def generate_match_summary(match_data: dict) -> str:
        """Generate match summary from match statistics"""
        try:
            # Extract basic data
            home_team = match_data.get('teams', {}).get('home', {}).get('name', 'Domácí')
            away_team = match_data.get('teams', {}).get('away', {}).get('name', 'Hosté')
            home_score = match_data.get('goals', {}).get('home', 0)
            away_score = match_data.get('goals', {}).get('away', 0)
            
            # Extract statistics if available
            statistics = match_data.get('statistics', [])
            home_stats_list = statistics[0].get('statistics', []) if len(statistics) > 0 else []
            away_stats_list = statistics[1].get('statistics', []) if len(statistics) > 1 else []

            # Build lookup dicts from [{type, value}] format
            home_stats = {s['type']: s['value'] for s in home_stats_list}
            away_stats = {s['type']: s['value'] for s in away_stats_list}

            def _int(val):
                if val is None:
                    return 0
                return int(str(val).replace('%', '') or 0)

            home_shots = _int(home_stats.get('Shots Total', home_stats.get('Total Shots', 0)))
            away_shots = _int(away_stats.get('Shots Total', away_stats.get('Total Shots', 0)))
            home_possession = _int(home_stats.get('Ball Possession', 50))
            away_possession = _int(away_stats.get('Ball Possession', 50))
            
            # Determine match type and get template
            summary = SummaryService._get_summary_from_stats(
                home_team, away_team, home_score, away_score,
                home_shots, away_shots, home_possession, away_possession
            )
            
            return summary
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Zápas se odehrál dle plánu. Podrobné statistiky najdete výše."
    
    @staticmethod
    def _get_summary_from_stats(home_team: str, away_team: str, home_score: int,
                                away_score: int, home_shots: int, away_shots: int,
                                home_possession: float, away_possession: float) -> str:
        """Get summary based on match statistics"""
        
        # Determine match type
        goal_diff = home_score - away_score
        shot_diff = home_shots - away_shots
        possession_diff = home_possession - away_possession
        
        # Win/Draw/Loss with dominance
        if home_score > away_score:
            if goal_diff >= 3 or (shot_diff >= 5 and possession_diff > 15):
                category = 'dominant_win'
            else:
                category = 'narrow_win'
        elif home_score < away_score:
            category = 'home_loss'
        else:
            category = 'draw'
        
        # Get random template
        import random
        template = random.choice(SummaryService.SUMMARY_TEMPLATES[category])
        
        # Format template with actual data
        summary = template.format(
            home_team=home_team,
            away_team=away_team,
            home_score=home_score,
            away_score=away_score,
            home_shots=home_shots,
            away_shots=away_shots,
            home_possession=int(home_possession),
            away_possession=int(away_possession)
        )
        
        return summary
    
    @staticmethod
    def generate_team_form_summary(last_matches: list) -> dict:
        """Generate team form summary from last matches"""
        if not last_matches or len(last_matches) == 0:
            return {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
        
        stats = {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
        
        for match in last_matches[:5]:  # Last 5 matches
            try:
                home_score = match.get('goals', {}).get('home', 0)
                away_score = match.get('goals', {}).get('away', 0)
                team_is_home = match.get('teams', {}).get('home', {}).get('id')
                
                if home_score > away_score:
                    if team_is_home:
                        stats['wins'] += 1
                        stats['goals_for'] += home_score
                        stats['goals_against'] += away_score
                    else:
                        stats['losses'] += 1
                        stats['goals_for'] += away_score
                        stats['goals_against'] += home_score
                elif home_score < away_score:
                    if team_is_home:
                        stats['losses'] += 1
                        stats['goals_for'] += home_score
                        stats['goals_against'] += away_score
                    else:
                        stats['wins'] += 1
                        stats['goals_for'] += away_score
                        stats['goals_against'] += home_score
                else:
                    stats['draws'] += 1
                    stats['goals_for'] += home_score
                    stats['goals_against'] += away_score
            except Exception as e:
                logger.error(f"Error processing match: {str(e)}")
                continue
        
        return stats

# Create singleton instance
summary_service = SummaryService()
