import styles from './style.module.css'
import { Container, LinkComponent } from '../index'

const Footer = () => {
  return <footer className={styles.footer}>
      <Container className={styles.footer__container}>
          <Container className={styles.footer__container}>
              <LinkComponent href='#' title='Продуктовый помощник' className={styles.footer__brand} />
          </Container>
          <Container className={styles.footer__container}>
              <LinkComponent href='#' title='Технологии' className={styles.footer__link} />
          </Container>
          <Container className={styles.footer__container}>
              <LinkComponent href='#' title='Об авторе' className={styles.footer__link} />
          </Container>
      </Container>
  </footer>
}

export default Footer
